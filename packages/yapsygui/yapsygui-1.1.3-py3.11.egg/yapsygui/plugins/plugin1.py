from qtpy.QtWidgets import QPushButton
from yapsy.IPlugin import IPlugin


class PluginOne(IPlugin):

    def __init__(self):
        super().__init__()
        self.context = None
        self.name = "Plugin test-01"

    def action(self, context):
        self.context = context
        button = QPushButton(self.name)
        button.clicked.connect(self.task)
        context.layout().addWidget(button)

    def task(self):
        self.context.output.append("This is a text from plugin test-01")