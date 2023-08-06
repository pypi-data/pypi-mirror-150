import json

from steamship import Tag
from steamship.app import App, Response, create_handler, post
from steamship.plugin.inputs.block_and_tag_plugin_input import BlockAndTagPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput
from steamship.plugin.service import PluginRequest
from steamship.plugin.tagger import Tagger


class TestParserPlugin(Tagger, App):
    # For testing; mirrors TestConfigurableTagger in Swift

    def run(
        self, request: PluginRequest[BlockAndTagPluginInput]
    ) -> Response[BlockAndTagPluginOutput]:
        tag_kind = self.config["tagKind"]  # TODO (enias): Review config loading
        tag_name = self.config["tagName"]
        tag_value = json.dumps(
            {
                "numberValue": self.config["numberValue"],
                "booleanValue": self.config["booleanValue"],
            }
        )

        if request.data is not None:
            file = request.data.file
            tag = Tag.CreateRequest(kind=tag_kind, name=tag_name, value=tag_value)
            if file.tags:
                file.tags.append(tag)
            else:
                file.tags = [tag]
            return Response(data=BlockAndTagPluginOutput(file))

    @post("tag")
    def parse(self, **kwargs) -> dict:
        parse_request = Tagger.parse_request(request=kwargs)
        return self.run(parse_request)


handler = create_handler(TestParserPlugin)
