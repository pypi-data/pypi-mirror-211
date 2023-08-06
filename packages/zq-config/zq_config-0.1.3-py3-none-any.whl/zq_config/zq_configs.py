from typing import cast
from importlib import import_module
from contextlib import suppress
from zq_config.backends import Backend

from zq_config.backends.backend_registry import BACKENDS_TYPES

def _try_import(module):
    lib = None
    with suppress(Exception):
        lib = import_module(module)
    return lib


class ZQ_Config:
    _backend: Backend = None
    _init: bool = False
    _json = None
    _toml = None

    @classmethod
    def __init__(cls, backend_type, **kwargs) -> None:
        if cls._init:
            return
        if backend_type not in BACKENDS_TYPES:
            raise Exception("Not found backend {}".format(backend_type))

        cls._backend = BACKENDS_TYPES[backend_type](**kwargs)

        # try import parsers
        cls._json = _try_import("json")
        cls._toml = _try_import("toml")

        cls._init = True

    @classmethod
    def get_raw(cls, data_id, data_group=None):
        return cls._backend.get(data_id, data_group)

    @classmethod
    def get_json(cls, data_id, data_group=None):
        data = cls._backend.get(data_id, data_group)
        if cls._json == None:
            raise Exception("json module is not install")
        return cls._json.loads(data)

    @classmethod
    def get_toml(cls, data_id, data_group=None):
        data = cls._backend.get(data_id, data_group)
        if cls._toml == None:
            raise Exception("toml module is not install")
        return cls._toml.loads(data)

    @classmethod
    def get(cls, data_id, data_group=None, format="json"):
        if format == "json":
            return cls.get_json(data_id, data_group)
        if format == "toml":
            return cls.get_toml(data_id, data_group)
        raise Exception("{} format is not support".format(format))
