"""# Notebook Modules
"""
import sys
from pathlib import Path
from ..hook import install_import_hook
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
    install_import_hook()
    cwd = Path.cwd()
    sys.path = [p for p in sys.path if Path(p).resolve() != cwd]
    ipython.user_ns.update({'__package__': determine_package_name(cwd), 'patch': patch})