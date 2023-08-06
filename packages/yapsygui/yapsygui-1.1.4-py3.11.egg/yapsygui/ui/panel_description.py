# -*- coding: utf-8 -*-

from qtpy.QtWidgets import QVBoxLayout, QLabel, QTextBrowser


class PanelDescription(QVBoxLayout):

    def __init__(self, parent):
        super().__init__(parent)
        self.setContentsMargins(10, 0, 0, 0)
        self.label_header = QLabel(parent)
        self.addWidget(self.label_header)

        self.description = QTextBrowser(parent)
        self.addWidget(self.description)

        self.label_header.setText(parent.tr("Plugin description"))
        self.description.setText(parent.tr("Description:"))
