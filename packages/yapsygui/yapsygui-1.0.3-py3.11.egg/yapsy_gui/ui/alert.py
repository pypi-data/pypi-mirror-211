from qtpy.QtWidgets import QDialog, QVBoxLayout, QLabel


class Alert(QDialog):

    def __init__(self, parent, text):
        super().__init__(parent)
        self.setModal(True)
        self.main_layout = QVBoxLayout(self)
        self.label = QLabel(self)
        text = parent.tr(text)
        self.label.setText(text)
        self.main_layout.addWidget(self.label)
        self.show()
