from string import Template

from yapsy.PluginInfo import PluginInfo

body = """
<h4>$name</h4>
<div>
    <ul>
        <li>Version: $version</li>
        <li>Author: $author</li>
        <li>Website: <a href="$website">$website</a></li>
    </ul>
</div>
<div>
    <p>$description</p>
</div>
"""


class PluginInfoTemplate(Template):

    def __init__(self):
        super().__init__(body)

    def substitute(self, data: PluginInfo):
        return super().substitute(
            name=data.name,
            version=data.version,
            author=data.author,
            website=data.website,
            description=data.description
        )
