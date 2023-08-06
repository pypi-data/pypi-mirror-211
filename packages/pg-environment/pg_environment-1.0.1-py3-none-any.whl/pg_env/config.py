from pg_common import SingletonBase
from pg_common import log_info, merge_dict, is_valid_ip
import os
from .define import *
import socket
import json


__auth__ = "baozilaji@gmail.com"
__all__ = ["config"]

__KEYS__ = ["SHELL", "PWD", "LOGNAME", "HOME", "LANG", "TERM", "USER", "OLDPWD"]


class _Config(SingletonBase):
    def __init__(self):
        self._conf = {}
        self._init()
        self._init_default()
        self._init_base()
        log_info(self._conf)

    def _init_base(self):
        # init host ip
        _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _sock.connect(('8.8.8.8', 80))
        _ip = _sock.getsockname()[0]
        if is_valid_ip(_ip):
            self.update(ENV_HOSTIP, _ip)

        # init work dir
        if not self.get_conf(ENV_PWD):
            self.update(ENV_PWD, os.getcwd())

        # init environ
        _work_dir = self.get_conf(ENV_PWD)
        _dir_name = _work_dir.split("/")[-1]
        self.update(ENV_ENVIRONMENT, EnvType.DEV.value)
        if _dir_name and len(_dir_name) > 0:
            if _dir_name.find("test") != -1:
                self.update(ENV_ENVIRONMENT, EnvType.TEST.value)
            elif _dir_name.find("prod") != -1:
                self.update(ENV_ENVIRONMENT, EnvType.PROD.value)

            # init port
            _port = _dir_name.split("_")[-1]
            if _port.isdigit():
                self.update(ENV_HOSTPORT, int(_port))

        # init from file
        _env_config_file = "%s/conf/%s.json" % (_work_dir, self.get_conf(ENV_ENVIRONMENT))
        if os.path.exists(_env_config_file):
            with open(_env_config_file, "r") as _f:
                merge_dict(self._conf, json.load(_f))

    def _init(self):
        for _k, _v in os.environ.items():
            if _k in __KEYS__:
                self.update(_k.lower(), _v)

    def _init_default(self):
        self.merge(DEFAULT_CONF)

    def update(self, key, value):
        if key is None:
            return
        if key in self._conf and isinstance(self._conf[key], dict):
            if isinstance(value, dict):
                merge_dict(self._conf[key], value)
            else:
                self._conf[key] = value
        else:
            self._conf[key] = value

    def merge(self, values):
        if isinstance(values, dict):
            merge_dict(self._conf, values)

    def get_conf(self, key):
        return self._conf.get(key)


config = _Config()
