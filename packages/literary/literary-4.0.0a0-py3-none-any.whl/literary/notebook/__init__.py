"""# Notebook Scripts
"""
from ..hook import install_import_hook
from ..transpile.patch import patch

def load_ipython_extension(ipython):
    """Load the import hook and setup the global state for the Literary extension.
    When IPython invokes this function, the determined package root path will be
    added to `sys.path`.

    :param ipython: IPython shell instance
    """
    install_import_hook()
    ipython.user_ns.update({'patch': patch})