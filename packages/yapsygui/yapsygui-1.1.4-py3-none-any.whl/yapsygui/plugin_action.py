import abc
import os.path as osp

from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QMainWindow, QAction
from yapsy.IPlugin import IPlugin
from .utils import findMainWindow


class APlugin(IPlugin, QAction):

    def __init__(self, path, text: str, icon: str, shortcut: str, tip: str):
        self.context = findMainWindow()
        self.path = path
        icon = self.getResource(icon)
        icon = QIcon(icon)
        IPlugin.__init__(self)
        QAction.__init__(self, icon, text, self.context)
        self.setShortcut(shortcut)
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.triggered.connect(self._parent)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'slot') and
                callable(subclass.slot) or
                NotImplemented)

    def _parent(self):
        self.slot(self.context)

    def getResource(self, resource):
        return osp.join(osp.dirname(osp.abspath(self.path)), resource)

    @abc.abstractmethod
    def slot(self, context: QMainWindow):
        raise NotImplementedError
