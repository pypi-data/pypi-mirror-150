"""# Notebook Finder
"""
import os
import pathlib
import sys
import traceback
import typing as tp
from importlib.machinery import FileFinder
from inspect import getclosurevars
from traitlets import Bool, Type
T = tp.TypeVar('T')

def _get_loader_details(hook) -> tuple:
    """Return the loader_details for a given FileFinder closure

    :param hook: FileFinder closure
    :returns: loader_details tuple
    """
    try:
        namespace = getclosurevars(hook)
    except TypeError as err:
        raise ValueError from err
    try:
        return namespace.nonlocals['loader_details']
    except KeyError as err:
        raise ValueError from err

def _find_file_finder(path_hooks: list) -> tp.Tuple[int, tp.Any]:
    """Find the FileFinder closure in a list of path hooks

    :param path_hooks: path hooks
    :returns: index of hook and the hook itself
    """
    for (i, hook) in enumerate(path_hooks):
        try:
            _get_loader_details(hook)
        except ValueError:
            continue
        return (i, hook)
    raise ValueError

def _derive_file_finder(finder: T, *loader_details) -> T:
    """Extend an existing file finder with new loader details

    :param finder: existing FileFinder instance
    :param loader_details:
    :return:
    """
    return FileFinder.path_hook(*_get_loader_details(finder), *loader_details)

def extend_file_finder(*loader_details):
    """Inject a set of loaders into a list of path hooks

    :param path_hooks: list of path hooks
    :param loader_details: FileFinder loader details
    :return:
    """
    (i, finder) = _find_file_finder(sys.path_hooks)
    sys.path_hooks[i] = _derive_file_finder(finder, *loader_details)
    sys.path_importer_cache.clear()