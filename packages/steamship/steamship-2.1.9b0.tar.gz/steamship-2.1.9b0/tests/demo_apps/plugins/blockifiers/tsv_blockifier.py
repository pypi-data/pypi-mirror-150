"""CSV Blockifier - Steamship Plugin."""

from typing import Any, Dict

from steamship.app import App, Response, create_handler, post
from steamship.plugin.blockifier import Blockifier
from tests.demo_apps.plugins.blockifiers.csv_blockifier import CsvBlockifier


class TsvBlockifier(CsvBlockifier, Blockifier, App):
    """Converts TSV into Tagged Steamship Blocks.

    Implementation is only here to demonstrate how plugins can be built through inheritance.
    """

    def __init__(self, client=None, config: Dict[str, Any] = None):
        super().__init__(client, config)
        self.config.delimiter = "\t"

    @post("blockify")  # TODO (enias): Move the blockify handle one inheritance level up
    def blockify(self, **kwargs) -> Response:
        """App endpoint for our plugin.

        The `run` method above implements the Plugin interface for a Converter.
        This `convert` method exposes it over an HTTP endpoint as a Steamship App.

        When developing your own plugin, you can almost always leave the below code unchanged.
        """
        blockify_request = Blockifier.parse_request(request=kwargs)
        return self.run(blockify_request)


handler = create_handler(TsvBlockifier)
