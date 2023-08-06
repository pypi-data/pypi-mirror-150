"""Remote Store Abstract Class."""
from __future__ import annotations

import logging
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import cast
from typing import Sequence

import proxystore as ps
from proxystore.proxy import Proxy
from proxystore.store.base import Store
from proxystore.store.base import StoreFactory
from proxystore.store.cache import LRUCache
from proxystore.store.exceptions import ProxyResolveMissingKey

logger = logging.getLogger(__name__)


class RemoteFactory(StoreFactory):
    """Factory for RemoteStore."""

    def __init__(
        self,
        key: str,
        store_type: type[Store],
        store_name: str,
        store_kwargs: dict[str, Any] | None = None,
        *,
        evict: bool = False,
        serialize: bool = True,
        strict: bool = False,
    ) -> None:
        """Init LocalFactory.

        Args:
            key (str): key corresponding to object in store.
            store_type (Store): type of store this factory will resolve
                an object from.
            store_name (str): name of store
            store_kwargs (dict): optional keyword arguments used to
                reinitialize store.
            evict (bool): If True, evict the object from the store once
                :func:`resolve()` is called (default: False).
            serialize (bool): if True, object in store is serialized and
                should be deserialized upon retrieval (default: True).
            strict (bool): guarantee object produce when this object is called
                is the most recent version of the object associated with the
                key in the store (default: False).
        """
        super().__init__(
            key,
            store_type=store_type,
            store_name=store_name,
            store_kwargs=store_kwargs,
            evict=evict,
            serialize=serialize,
            strict=strict,
        )

        # super() will have already initialized these dynamically but add
        # types so mypy know what they are/that they exist
        self.serialize: bool
        self.strict: bool

    def _get_value(self) -> Any:
        """Get the value associated with the key from the store."""
        store = cast(RemoteStore, self.get_store())
        obj = store.get(
            self.key,
            deserialize=self.serialize,
            strict=self.strict,
        )

        if obj is None:
            raise ProxyResolveMissingKey(
                self.key,
                self.store_type,
                self.store_name,
            )

        if self.evict:
            store.evict(self.key)

        return obj

    def _should_resolve_async(self) -> bool:
        """Check if it makes sense to do asynchronous resolution."""
        return not cast(RemoteStore, self.get_store()).is_cached(
            self.key,
            strict=self.strict,
        )


class RemoteStore(Store, metaclass=ABCMeta):
    """Abstraction for interacting with a remote key-value store.

    Provides base functionality for interaction with a remote store including
    serialization and caching.
    Subclasses of :class:`RemoteStore` must implement
    :func:`evict() <Store.evict()>`, :func:`exists() <Store.exists()>`,
    :func:`get_str()`, :func:`set_str()` and :func:`proxy() <Store.proxy()>`.
    The :class:`RemoteStore` handles the caching.

    :class:`RemoteStore` stores key-string pairs, i.e., objects passed to
    :func:`get()` or :func:`set()` will be appropriately (de)serialized.
    Functionality for serialized, caching, and strict guarantees are already
    provided in :func:`get()` and :func:`set()`.
    """

    def __init__(
        self,
        name: str,
        *,
        cache_size: int = 16,
        **kwargs: Any,
    ) -> None:
        """Init RemoteStore.

        Args:
            name (str): name of the store instance.
            cache_size (int): size of local cache (in # of objects). If 0,
                the cache is disabled (default: 16).
            kwargs (dict): additional keyword arguments to pass to
                :class:`BaseStore <proxystore.store.base.Store>`.

        Raises:
            ValueError:
                if `cache_size` is negative.
        """
        if cache_size < 0:
            raise ValueError('Cache size cannot be negative')
        self.cache_size = cache_size
        self._cache = LRUCache(cache_size)
        super().__init__(name, **kwargs)

    def _kwargs(
        self,
        kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Helper for handling inheritance with kwargs property.

        Args:
            kwargs (optional, dict): dict to use as return object. If None,
                a new dict will be created.
        """
        if kwargs is None:
            kwargs = {}  # pragma: no cover
        kwargs.update({'cache_size': self.cache_size})
        return super()._kwargs(kwargs)

    @abstractmethod
    def get_bytes(self, key: str) -> bytes | None:
        """Get serialized object from remote store.

        Args:
            key (str): key corresponding to object.

        Returns:
            serialized object or `None` if it does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def set_bytes(self, key: str, data: bytes) -> None:
        """Set serialized object in remote store with key.

        Args:
            key (str): key corresponding to object.
            data (bytes): serialized object.
        """
        raise NotImplementedError

    def get(
        self,
        key: str,
        *,
        deserialize: bool = True,
        strict: bool = False,
        default: Any | None = None,
    ) -> Any | None:
        """Return object associated with key.

        Args:
            key (str): key corresponding to object.
            deserialize (bool): deserialize object if True. If objects
                are custom serialized, set this as False (default: True).
            strict (bool): guarantee returned object is the most recent
                version (default: False).
            default: optionally provide value to be returned if an object
                associated with the key does not exist (default: None).

        Returns:
            object associated with key or `default` if key does not exist.
        """
        if self.is_cached(key, strict=strict):
            value = self._cache.get(key)['value']
            logger.debug(
                f"GET key='{key}' FROM {self.__class__.__name__}"
                f"(name='{self.name}'): was_cached=True",
            )
            return value

        value = self.get_bytes(key)
        if value is not None:
            timestamp = self.get_timestamp(key)
            if deserialize:
                value = ps.serialize.deserialize(value)
            self._cache.set(key, {'timestamp': timestamp, 'value': value})
            logger.debug(
                f"GET key='{key}' FROM {self.__class__.__name__}"
                f"(name='{self.name}'): was_cached=False",
            )
            return value

        logger.debug(
            f"GET key='{key}' FROM {self.__class__.__name__}"
            f"(name='{self.name}'): key did not exist, returned default",
        )
        return default

    def get_timestamp(self, key: str) -> float:
        """Get timestamp of most recent object version in the store."""
        raise NotImplementedError

    def is_cached(self, key: str, *, strict: bool = False) -> bool:
        """Check if object is cached locally.

        Args:
            key (str): key corresponding to object.
            strict (bool): guarantee object in cache is most recent version
                (default: False).

        Returns:
            bool
        """
        if self._cache.exists(key):
            if strict:
                store_timestamp = self.get_timestamp(key)
                cache_timestamp = self._cache.get(key)['timestamp']
                return cache_timestamp >= store_timestamp
            return True

        return False

    def proxy(  # type: ignore[override]
        self,
        obj: Any | None = None,
        *,
        key: str | None = None,
        factory: type[RemoteFactory] = RemoteFactory,
        **kwargs: Any,
    ) -> ps.proxy.Proxy:
        """Create a proxy that will resolve to an object in the store.

        Args:
            obj (object): object to place in store and return proxy for.
                If an object is not provided, a key must be provided that
                corresponds to an object already in the store (default: None).
            key (str): optional key to associate with `obj` in the store.
                If not provided, a key will be generated (default: None).
            factory (Factory): factory class that will be instantiated
                and passed to the proxy. The factory class should be able
                to correctly resolve the object from this store.
            kwargs (dict): additional arguments to pass to the Factory.

        Returns:
            :any:`Proxy <proxystore.proxy.Proxy>`

        Raises:
            ValueError:
                if `key` and `obj` are both `None`.
        """
        if obj is not None:
            if 'serialize' in kwargs:
                final_key = self.set(
                    obj,
                    key=key,
                    serialize=kwargs['serialize'],
                )
            else:
                final_key = self.set(obj, key=key)
        elif key is not None:
            final_key = key
        else:
            raise ValueError('At least one of key or obj must be specified')
        logger.debug(
            f"PROXY key='{final_key}' FROM {self.__class__.__name__}"
            f"(name='{self.name}')",
        )
        return Proxy(
            factory(
                final_key,
                store_name=self.name,
                store_kwargs=self.kwargs,
                **kwargs,
            ),
        )

    def proxy_batch(  # type: ignore[override]
        self,
        objs: Sequence[Any] | None = None,
        *,
        keys: Sequence[str] | None = None,
        factory: type[RemoteFactory] | None = None,
        **kwargs: Any,
    ) -> list[ps.proxy.Proxy]:
        """Create proxies for batch of objects in the store.

        See :any:`proxy() <proxystore.store.base.Store.proxy>` for more
        details.

        Args:
            objs (Sequence[Any]): objects to place in store and return
                proxies for. If an iterable of objects is not provided, an
                iterable of keys must be provided that correspond to objects
                already in the store (default: None).
            keys (Sequence[str]): optional keys to associate with `objs` in the
                store. If not provided, keys will be generated (default: None).
            factory (Factory): Optional factory class that will be instantiated
                and passed to the proxies. The factory class should be able
                to correctly resolve an object from this store. Defaults to
                None so the default of :func:`proxy()` is used.
            kwargs (dict): additional arguments to pass to the Factory.

        Returns:
            List of :any:`Proxy <proxystore.proxy.Proxy>`

        Raises:
            ValueError:
                if `keys` and `objs` are both `None`.
            ValueError:
                if `objs` is None and `keys` does not exist in the store.
        """
        if objs is not None:
            if 'serialize' in kwargs:
                final_keys = self.set_batch(
                    objs,
                    keys=keys,
                    serialize=kwargs['serialize'],
                )
            else:
                final_keys = self.set_batch(objs, keys=keys)
        elif keys is not None:
            final_keys = list(keys)
        else:
            raise ValueError('At least one of keys or objs must be specified')
        if factory is not None:
            kwargs['factory'] = factory
        return [self.proxy(None, key=key, **kwargs) for key in final_keys]

    def set(
        self,
        obj: Any,
        *,
        key: str | None = None,
        serialize: bool = True,
    ) -> str:
        """Set key-object pair in store.

        Args:
            obj (object): object to be placed in the store.
            key (str, optional): key to use with the object. If the key is not
                provided, one will be created.
            serialize (bool): serialize object if True. If object is already
                custom serialized, set this as False (default: True).

        Returns:
            key (str)
        """
        if serialize:
            obj = ps.serialize.serialize(obj)
        if key is None:
            key = self.create_key(obj)

        self.set_bytes(key, obj)
        logger.debug(
            f"SET key='{key}' IN {self.__class__.__name__}"
            f"(name='{self.name}')",
        )
        return key

    def set_batch(
        self,
        objs: Sequence[Any],
        *,
        keys: Sequence[str | None] | None = None,
        serialize: bool = True,
    ) -> list[str]:
        """Set objects in store.

        Args:
            objs (Sequence[Any]): iterable of objects to be placed in the
                store.
            keys (Sequence[str], optional): keys to use with the objects.
                If the keys are not provided, keys will be created.
            serialize (bool): serialize object if True. If object is already
                custom serialized, set this as False (default: True).

        Returns:
            List of keys (str). Note that some implementations of a store may
            return keys different from the provided keys.

        Raises:
            ValueError:
                if :code:`keys is not None` and :code:`len(objs) != len(keys)`.
        """
        if keys is not None and len(objs) != len(keys):
            raise ValueError(
                f'objs has length {len(objs)} but keys has length {len(keys)}',
            )
        if keys is None:
            keys = [None] * len(objs)

        return [
            self.set(obj, key=key, serialize=serialize)
            for key, obj in zip(keys, objs)
        ]
