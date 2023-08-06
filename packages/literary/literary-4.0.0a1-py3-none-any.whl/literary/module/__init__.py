"""# Notebook Modules
"""
import sys
import warnings
from pathlib import Path
from ..transpile.patch import patch

def determine_package_name(path: Path) -> str:
    """Determine the corresponding importable name for a package directory given by
    a particular file path. Return `None` if path is not contained within `sys.path`.

    :param path: path to package
    :return:
    """
    for p in sys.path:
        if str(path) == p:
            continue
        try:
            relative_path = path.relative_to(p)
        except ValueError:
            continue
        return '.'.join(relative_path.parts)
    return None

def load_ipython_extension(ipython):
    """Load the import hook and setup the global state for the Literary extension.
    When IPython invokes this function, the determined package root path will be
    added to `sys.path`.

    :param ipython: IPython shell instance
    """
    cwd = Path.cwd()
    sys.path = [p for p in sys.path if Path(p).resolve() != cwd]
    package = determine_package_name(cwd)
    if package is None:
        warnings.warn(f"Couldn't determine the package name for the current working directory {cwd}. This might be because the current project has not been installed in editable mode.")
    ipython.user_ns.update({'__package__': determine_package_name(cwd), 'patch': patch})