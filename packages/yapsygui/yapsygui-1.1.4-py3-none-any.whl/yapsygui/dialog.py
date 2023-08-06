#############################################################################
#
#   Source Yapsy:
#   https://github.com/tibonihoo/yapsy
#
#   GUI implemented by: Leonel Hernández
#   Source: https://github.com/leonelhs/yapsy-gui
#
##############################################################################
import os
import os.path as osp
from yapsygui import Manager, PluginInfoTemplate
from yapsygui.ui import DialogPluginsBase, Alert, OpenFilePlugin

INVALID_STRUCTURE = "Plugin structure is not valid."
REMOVE_ERROR = "Unable to uninstall plugin."


def getPath(path):
    dir_path = osp.dirname(osp.abspath(path))
    dir_path = osp.join(dir_path, "plugins")
    if not osp.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


class DialogPlugins(DialogPluginsBase):

    def __init__(self, parent, install_dir):
        super().__init__(parent)
        self.callback = None
        install_dir = getPath(install_dir)
        self.manager = Manager(install_dir)
        self.template = PluginInfoTemplate()

    @property
    def plugins(self):
        return self.manager.plugins

    def connect(self, callback):
        self.callback = callback

    def installPlugin(self):
        plugin_file = OpenFilePlugin(self)
        if plugin_file:
            if self.manager.install(plugin_file):
                self.loadPlugins()
            else:
                Alert(self, INVALID_STRUCTURE)

    def uninstallPlugin(self):
        if self.manager.removePlugin(self.plugin):
            self.loadPlugins()
        else:
            Alert(self, REMOVE_ERROR)

    def loadPlugins(self):
        try:
            # Fixme: After install a new plugin, not always reloads the plugins
            self.manager = Manager(self.manager.install_dir)
            self.callback(self.plugins)
        except TypeError:
            print("No plugins loader callback was defined.")
        finally:
            self.panel.appendPlugins(self.plugins)

    def onSelectPlugin(self, data):
        data = self.template.substitute(data)
        self.panel.description.setText(data)
