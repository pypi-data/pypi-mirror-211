from zq_config.backends import Backend
import ttl_cache
from importlib import import_module

class NacosBackend(Backend):
    _client = None

    def __init__(self, **kwargs) -> None:
        self._client = import_module("nacos").NacosClient(**kwargs)

    @ttl_cache
    def get(self, data_id, data_group="DEFAULT_GROUP"):
        return self._client.get_config(data_id, data_group)
