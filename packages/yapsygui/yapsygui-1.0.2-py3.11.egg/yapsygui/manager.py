import os
import shutil

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from yapsy.AutoInstallPluginManager import AutoInstallPluginManager

INFO_EXTENSION = "plugin"
PLUGINS_CATEGORY = "Default"


class Installer(AutoInstallPluginManager):

    def __init__(self, install_dir):
        super().__init__(plugin_info_ext=INFO_EXTENSION)
        self.setInstallDir(install_dir)

    def install(self, plugin_file):
        plugin_dir = os.path.dirname(plugin_file)
        try:
            if super().install(plugin_dir, plugin_file):
                return True
        except ValueError:
            return False


class Manager(PluginManager):

    def __init__(self, install_dir):
        super().__init__()
        self.install_dir = install_dir
        self.setPluginPlaces([self.install_dir])
        self.setCategoriesFilter({PLUGINS_CATEGORY: IPlugin})
        self.setPluginInfoExtension(INFO_EXTENSION)
        self._installer = Installer(self.install_dir)

    @property
    def plugins(self):
        self.collectPlugins()
        return self.getAllPlugins()

    def install(self, plugin_file):
        return self._installer.install(plugin_file)

    def removePlugin(self, plugin):
        self.removePluginFromCategory(plugin, PLUGINS_CATEGORY)
        prefix = os.path.basename(plugin.path)
        for item in os.listdir(self.install_dir):
            if item.startswith(prefix):
                item = os.path.join(self.install_dir, item)
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
        return True
