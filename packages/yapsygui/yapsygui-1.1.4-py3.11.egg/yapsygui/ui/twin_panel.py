# -*- coding: utf-8 -*-

from qtpy.QtGui import QStandardItemModel
from qtpy.QtWidgets import QSplitter, QWidget
from qtpy.QtCore import Qt
from yapsy.PluginInfo import PluginInfo

from yapsygui import PluginItem
from yapsygui.ui import PanelPlugins, PanelDescription


class TwinPanel(QSplitter):

    def __init__(self, parent):
        super().__init__(parent)
        self.callback = None
        self.current_item = None
        self.setOrientation(Qt.Horizontal)

        self.widget_left = QWidget(self)
        self.panel_plugins = PanelPlugins(self.widget_left)
        self.addWidget(self.widget_left)

        self.widget_right = QWidget(self)
        self.panel_description = PanelDescription(self.widget_right)
        self.addWidget(self.widget_right)
        self.model = QStandardItemModel(self.list)
        self.setModel(self.model)

        self.list.clicked.connect(self.onSelectPlugin)

    @property
    def plugin(self):
        return self.current_item

    @property
    def list(self):
        return self.panel_plugins.list

    @property
    def description(self):
        return self.panel_description.description

    def onSelectPlugin(self, index):
        self.current_item = self._item(index)
        self.callback(self.current_item)

    def connect(self, callback):
        self.callback = callback

    def setModel(self, model):
        self.list.setModel(model)

    def appendRow(self, item):
        self.model.appendRow(item)

    def appendPlugins(self, plugins):
        self.clear()
        for plugin in plugins:
            item = PluginItem(plugin)
            self.appendRow(item)

    def clear(self):
        self.model.clear()
        self.description.clear()

    def _item(self, index) -> PluginInfo:
        row = index.row()
        return self.model.item(row).info()
