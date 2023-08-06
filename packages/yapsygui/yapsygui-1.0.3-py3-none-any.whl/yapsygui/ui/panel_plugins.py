# -*- coding: utf-8 -*-

from qtpy.QtCore import QCoreApplication
from qtpy.QtWidgets import QVBoxLayout, QLabel, QListView


class PanelPlugins(QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.label_plugins = QLabel(parent)
        self.addWidget(self.label_plugins)
        self.list = QListView(parent)
        self.addWidget(self.list)
        self.label_plugins.setText(QCoreApplication.translate("Dialog", u"Installed plugins", None))
