from zq_config.backends import Backend, get_dependency
import ttl_cache

class NacosBackend(Backend):
    _client = None

    def __init__(self, **kwargs) -> None:
        self._client = get_dependency("nacos").NacosClient(**kwargs)

    @ttl_cache
    def get(self, data_id, data_group="DEFAULT_GROUP"):
        return self._client.get_config(data_id, data_group)
