import codecs
import json
import os
import pathlib
import configparser
from types import SimpleNamespace
from typing import Union

import yaml

from libs.Config.config_provider import _ConfigProvider


class Config:
    # If no value is found, it tries to get a value from the environment, otherwise an exception is thrown.

    @staticmethod
    def load(path: Union[str, os.PathLike]) -> _ConfigProvider:
        if isinstance(path, os.PathLike):
            path = os.fspath(path)

        if not os.path.exists(path):
            raise FileNotFoundError(f"File '{path}' not found!")

        suffix = path.split(".")[-1]

        suffixes_dict = {
            "yaml": Config._load_yaml,
            "json": Config._load_json,
            "ini": Config._load_ini,
            "toml": Config._load_toml,
        }

        if suffix in suffixes_dict:
            return suffixes_dict[suffix](path)
        else:
            raise ValueError(f"The file with the extension '{suffix}' is not supported!")

    @staticmethod
    def _load_yaml(path: str) -> _ConfigProvider:
        # .yaml
        with open(path, "r", encoding="utf-8") as file:
            config = _ConfigProvider(path, yaml.load(file, Loader=yaml.FullLoader))

        return config

    @staticmethod
    def _load_json():
        # .json
        pass

    @staticmethod
    def _load_ini():
        # .ini
        pass

    @staticmethod
    def _load_toml():
        # .toml
        pass
