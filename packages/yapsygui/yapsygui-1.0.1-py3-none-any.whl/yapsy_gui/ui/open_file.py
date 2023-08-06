from qtpy.QtWidgets import QFileDialog

init_path = ""
file_filter = "*.plugin"


class OpenFilePlugin(QFileDialog):

    def __new__(cls, parent, flags=None):
        title = parent.tr("Install Plugin")
        file_name, _ = cls.getOpenFileName(parent, title, init_path, file_filter)
        return file_name
