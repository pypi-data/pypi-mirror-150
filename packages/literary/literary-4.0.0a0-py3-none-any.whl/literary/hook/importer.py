"""# Import Hook
"""
from nbconvert import Exporter
from traitlets import Instance, Type, default
from traitlets.config import Configurable
from ..transpile.exporter import LiteraryExporter
from .loader import NotebookLoader

class NotebookImporter(Configurable):
    exporter = Instance(Exporter)
    exporter_class = Type(LiteraryExporter).tag(config=True)

    @default('exporter')
    def _exporter_default(self):
        return self.exporter_class(parent=self)

    def get_loader(self, fullname, path):
        exporter = self.exporter_class(parent=self)
        return NotebookLoader(fullname, path, exporter=self.exporter)