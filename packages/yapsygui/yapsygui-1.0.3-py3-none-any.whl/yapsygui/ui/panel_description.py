# -*- coding: utf-8 -*-

from qtpy.QtCore import QCoreApplication
from qtpy.QtWidgets import QVBoxLayout, QLabel, QTextBrowser


class PanelDescription(QVBoxLayout):

    def __init__(self, parent):
        super().__init__(parent)
        self.setContentsMargins(10, 0, 0, 0)
        self.label_header = QLabel(parent)
        self.addWidget(self.label_header)

        self.description = QTextBrowser(parent)
        self.addWidget(self.description)

        self.label_header.setText(QCoreApplication.translate("Dialog", u"Plugin description", None))
        self.description.setText(QCoreApplication.translate("Dialog", u"Description:", None))
