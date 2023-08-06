""""""
from .finder import extend_file_finder
from ..config import load_literary_config, find_literary_config
import functools
import sys
import traceback
import pathlib
load_cached_config = functools.lru_cache()(load_literary_config)

def install_import_hook(set_except_hook=True):

    def create_notebook_loader(fullname, path):
        from .importer import NotebookImporter
        config = load_cached_config(find_literary_config(pathlib.Path(path)))
        print('Loaded', path)
        importer = NotebookImporter(config=config)
        return importer.get_loader(fullname, path)
    extend_file_finder((create_notebook_loader, ['.ipynb']))
    if set_except_hook:
        sys.excepthook = traceback.print_exception