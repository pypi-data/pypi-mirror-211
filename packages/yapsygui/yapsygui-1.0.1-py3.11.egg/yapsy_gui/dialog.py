#############################################################################
#
#   Source Yapsy:
#   https://github.com/tibonihoo/yapsy
#
#   GUI implemented by: Leonel Hernández
#   Source: https://github.com/leonelhs/yapsy-gui
#
##############################################################################
from yapsy_gui import Manager, PluginItem, PluginInfoTemplate
from yapsy_gui.ui import DialogPluginsBase, Alert, OpenFilePlugin

INVALID_STRUCTURE = "Plugin structure is not valid."


class DialogPlugins(DialogPluginsBase):

    def __init__(self, parent, install_dir):
        super().__init__(parent)
        self.install_dir = install_dir
        self.manager = Manager(install_dir)
        self.template = PluginInfoTemplate()
        self.displayPlugins()

    @property
    def plugins(self):
        return self.manager.plugins

    def installPlugin(self):
        plugin_file = OpenFilePlugin(self)
        if plugin_file:
            if self.manager.install(plugin_file):
                self.pluginsUpdate.emit()
            else:
                Alert(self, INVALID_STRUCTURE)

    def uninstallPlugin(self):
        self.manager.removePlugin(self.panel.plugin)
        # Fixme: Reload plugins list instead of reload Manager after delete plugin
        self.manager = Manager(self.install_dir)
        self.pluginsUpdate.emit()

    def displayPlugins(self):
        self.panel.clear()
        for candidate in self.plugins:
            item = PluginItem(candidate)
            self.panel.appendRow(item)

    def onSelectPlugin(self, data):
        data = self.template.substitute(data)
        self.panel.description.setText(data)
