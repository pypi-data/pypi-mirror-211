import abc
import os
import typing
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QMainWindow, QApplication, QAction
from yapsy.IPlugin import IPlugin


def findMainWindow() -> typing.Union[QMainWindow, None]:
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None


def getResource(resource):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(dir_path, "plugins")
    return os.path.join(dir_path, resource)


class APlugin(IPlugin, QAction):

    def __init__(self, text: str, icon: str, shortcut: str, tip: str):
        self.context = findMainWindow()
        icon = getResource(icon)
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

    @abc.abstractmethod
    def slot(self, context: QMainWindow):
        raise NotImplementedError
