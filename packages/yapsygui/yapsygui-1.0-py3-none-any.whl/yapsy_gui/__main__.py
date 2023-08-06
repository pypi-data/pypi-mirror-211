#############################################################################
#
#   Source Yapsy:
#   https://github.com/tibonihoo/yapsy
#
#   GUI implemented by: Leonel Hernández
#   Source: https://github.com/leonelhs/yapsy-gui
#
##############################################################################
import sys
from qtpy import QtWidgets
from qtpy.QtWidgets import QMainWindow, QWidget, \
    QVBoxLayout, QLabel, QPushButton, QTextBrowser
from yapsy_gui import DialogPlugins


# Fixme: Reload list plugins on uninstall plugin

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.label = QLabel(self)
        self.label.setText("Yapsy GUI Plugin Manager")
        self.main_layout.addWidget(self.label)
        self.button_plugins = QPushButton(self)
        self.button_plugins.setText("Show Plugin Manager")
        self.button_plugins.clicked.connect(self.showPlugins)
        self.main_layout.addWidget(self.button_plugins)
        self.setCentralWidget(self.central_widget)
        # Yapsy plugin manager API is embedded in GUI
        self.manager = DialogPlugins(self)
        self.manager.pluginsUpdate.connect(self.fetchPlugins)
        self.fetchPlugins()

        self.output = QTextBrowser(self.central_widget)
        self.main_layout.addWidget(self.output)

    def fetchPlugins(self):
        for plugin in self.manager.plugins:
            plugin.plugin_object.context = self
            button = QPushButton(self)
            button.setText(plugin.plugin_object.name)
            button.clicked.connect(plugin.plugin_object.task)
            self.main_layout.addWidget(button)
        self.manager.displayPlugins()

    # Plugin callback: make the process at plugin and it putback here the result
    def plugin_action(self, text):
        self.output.append(text)

    def showPlugins(self):
        self.manager.show()


def main():
    app = QtWidgets.QApplication()
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
