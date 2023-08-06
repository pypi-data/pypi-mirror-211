from yapsy.IPlugin import IPlugin


class PluginOne(IPlugin):

    def __init__(self):
        super().__init__()
        self.context = None
        self.name = "Plugin test-01"

    def task(self):
        self.context.plugin_action("This is a text from plugin test-01")