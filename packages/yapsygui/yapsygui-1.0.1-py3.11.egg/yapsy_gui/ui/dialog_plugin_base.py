from abc import abstractmethod

from qtpy.QtCore import QMetaObject, Signal
from qtpy.QtWidgets import QDialog, QVBoxLayout

from yapsy_gui.ui import TwinPanel, RowButtons

TITLE = "Plugins Manager"


class DialogPluginsBase(QDialog):
    pluginsUpdate = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.tr = parent.tr
        self.setModal(True)

        self.main_layout = QVBoxLayout(self)
        self.panel = TwinPanel(self)
        self.main_layout.addWidget(self.panel)
        self.controls = RowButtons(self)
        self.main_layout.addLayout(self.controls)
        self.controls.install.connect(self.installPlugin)
        self.controls.uninstall.connect(self.uninstallPlugin)
        self.panel.connect(self.onSelectPlugin)

        QMetaObject.connectSlotsByName(self)

        self.setWindowTitle(self.tr(TITLE))

    @abstractmethod
    def installPlugin(self):
        pass

    @abstractmethod
    def uninstallPlugin(self):
        pass

    @abstractmethod
    def onSelectPlugin(self, data):
        pass
