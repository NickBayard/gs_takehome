from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from yaml import safe_load, YAMLObject, SafeLoader


class ConfigError(Exception):
    pass

CONFIG_ENV_VARIABLE = 'CONFIG_PATH'
DEFAULT_CONFIG_PATH = Path(__file__).parent / '../config.yaml'

class Config(YAMLObject):
    yaml_tag = '!Config'
    _config: Any | Config = None

    def __init__(self, database_type):
        self.database_type = database_type

    def __repr__(self):
        return f'{self.__class__.__name__}(database_type={self.database_type})'

    @classmethod
    def construct(cls, loader, node) -> Config:
        return cls(**loader.construct_mapping(node))

    @classmethod
    def build(cls, file: str | None = None) -> None:
        """
        Attempt to parse the configuration from the yaml config file
        and cache to the class.  The configuration file maybe specified
        in multiple ways using the following priority:
        - classmethod parameter (not used by Config.get())
        - environment variable
        - default hardcoded path (fallback)
        """
        path = None
        if file is None:
            # try to get from env variable
            file = os.environ.get(CONFIG_ENV_VARIABLE)
        if file is not None:
            path = Path(file)

        if path is None:
            # fallback to default path
            path = DEFAULT_CONFIG_PATH


        if not path.is_file():
            raise ConfigError(f'Invalid config file: {path}. {Path.cwd()}')

        with path.open() as f:
            cls._config = safe_load(f)

    @classmethod
    def get(cls) -> Any | Config:
        if cls._config is None:
            cls.build()
        return cls._config

SafeLoader.add_constructor('!Config', Config.construct)