import os
from string import Template

from yapsy.PluginInfo import PluginInfo

dir_path = os.path.dirname(os.path.abspath(__file__))
template = os.path.join(dir_path, "template.html")


class PluginInfoTemplate(Template):

    def __init__(self):
        with open(template) as body:
            super().__init__(body.read())

    def substitute(self, data: PluginInfo):
        return super().substitute(
            name=data.name,
            version=data.version,
            author=data.author,
            website=data.website,
            description=data.description
        )
