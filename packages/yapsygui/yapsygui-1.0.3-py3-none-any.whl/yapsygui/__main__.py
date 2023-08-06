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
import sys

from qtpy import QtWidgets
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextBrowser

from yapsygui import DialogPlugins

# Default demo plugins location path
location = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.join(location, "plugins")


def fetchPlugins(plugins):
    for plugin in plugins:
        plugin.plugin_object.action(win)


app = QtWidgets.QApplication()
win = QWidget(None)
win.setLayout(QVBoxLayout())
btn_manager = QPushButton("Show Manager")
win.layout().addWidget(btn_manager)

manager = DialogPlugins(win, INSTALL_DIR)
manager.connect(fetchPlugins)
manager.loadPlugins()

btn_manager.clicked.connect(manager.show)
win.output = QTextBrowser(win)
win.layout().addWidget(win.output)

win.show()
sys.exit(app.exec_())
