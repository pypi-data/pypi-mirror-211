# -*- coding: utf-8 -*-

from qtpy.QtGui import QStandardItem
from yapsy.PluginInfo import PluginInfo


class PluginItem(QStandardItem):

    def __init__(self, plugin: PluginInfo):
        super().__init__()
        self.plugin = plugin
        self.setEditable(False)
        self.setText(self.plugin.name)

    def info(self) -> PluginInfo:
        return self.plugin
