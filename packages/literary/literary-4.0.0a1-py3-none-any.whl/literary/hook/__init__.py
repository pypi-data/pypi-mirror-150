""""""
from .finder import extend_file_finder
import sys
import traceback
import pathlib

def notebook_loader_factory(fullname, path):
    try:
        factory = notebook_loader_factory.factory
    except AttributeError:

        def noop_loader(fullname, path):
            return None
        notebook_loader_factory.factory = noop_loader
        from .importer import get_loader
        notebook_loader_factory.factory = get_loader
        factory = get_loader
    return factory(fullname, path)

def install_import_hook(set_except_hook=True):
    extend_file_finder((notebook_loader_factory, ['.ipynb']))
    if set_except_hook:
        sys.excepthook = traceback.print_exception