import os
from typing import Union, Optional, Any

import yaml


class _ConfigProvider:

    def __init__(self, path: Union[str, os.PathLike], dictionary: dict):
        self._path = path
        self._dict = dictionary

    def get(self, key: str, default: Optional[Any] = ...):
        args = key.split('.')
        branch = self._dict

        try:
            for arg in args:
                branch = branch[arg]
        except KeyError as e:
            if default is ...:
                if key in os.environ:
                    return os.getenv(key)
                raise ValueError(f"The key '{key}' in the configuration file '{self._path}' was not found") from e
            return default
        return branch

    def __getitem__(self, key: str):
        # Alias to get()
        return self.get(key)

    def set(self, key: str, value):
        args = key.split('.')
        branch = self._dict
        for arg in args[:-1]:
            branch = branch[arg]
        branch[args[-1]] = value

    def __setitem__(self, key: str, value):
        # Alias to set()
        self.set(key, value)

    def save(self):
        suffix = self._path.split(".")[-1]

        if suffix == "yaml":
            with open(self._path, "w", encoding="utf-8") as file:
                file.write(yaml.dump(self._dict, allow_unicode=True))
