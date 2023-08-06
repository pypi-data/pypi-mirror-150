""""""
import typing as tp
from functools import lru_cache
from pathlib import Path
from traitlets.config import Config, ConfigFileNotFound, JSONFileConfigLoader, PyFileConfigLoader
CONFIG_FILE_STEM = 'literary_config'

@lru_cache()
def find_literary_config(path, *additional_paths) -> Path:
    """Load the configuration for the current Literary project.

    :param search_paths: starting search paths
    :return:
    """
    visited = set()
    for top_level_path in [path, *additional_paths]:
        for search_path in (top_level_path, *top_level_path.parents):
            if search_path in visited:
                break
            visited.add(search_path)
            for p in search_path.glob(f'{CONFIG_FILE_STEM}.*'):
                return p
    raise FileNotFoundError("Couldn't find config file")

def load_literary_config(path: Path) -> Config:
    """Load a project configuration file

    :param path: configuration file path
    :return:
    """
    for loader_cls in (JSONFileConfigLoader, PyFileConfigLoader):
        loader = loader_cls(path.name, str(path.parent))
        try:
            config = loader.load_config()
            break
        except ConfigFileNotFound:
            continue
    else:
        raise ValueError(f'{path!r} was not a recognised config file')
    return config