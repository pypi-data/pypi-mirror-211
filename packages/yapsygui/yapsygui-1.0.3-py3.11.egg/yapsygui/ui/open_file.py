import os

from qtpy.QtWidgets import QFileDialog


class OpenFilePlugin(QFileDialog):

    def __new__(cls, parent, flags=None):
        title = parent.tr("Install Plugin")
        init_path = os.path.expanduser('~')
        file_filter = "*.plugin"
        file_name, _ = cls.getOpenFileName(parent, title, init_path, file_filter)
        return file_name
