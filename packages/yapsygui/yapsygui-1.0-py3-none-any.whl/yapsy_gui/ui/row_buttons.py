# -*- coding: utf-8 -*-

from qtpy.QtCore import QCoreApplication
from qtpy.QtWidgets import QHBoxLayout, QPushButton


class RowButtons(QHBoxLayout):

    def __init__(self, parent):
        super().__init__(parent)
        self.button_install = QPushButton(parent)
        self.addWidget(self.button_install)
        self.button_uninstall = QPushButton(parent)
        self.addWidget(self.button_uninstall)
        self.button_install.setText(QCoreApplication.translate("Dialog", u"Install plugin", None))
        self.button_uninstall.setText(QCoreApplication.translate("Dialog", u"Remove plugin", None))

    @property
    def install(self):
        return self.button_install.clicked

    @property
    def uninstall(self):
        return self.button_uninstall.clicked
