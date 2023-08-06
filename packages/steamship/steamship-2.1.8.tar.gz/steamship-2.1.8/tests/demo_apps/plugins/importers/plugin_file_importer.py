from typing import Any

from steamship import MimeTypes
from steamship.app import App, Response, create_handler, post
from steamship.extension.file import File
from steamship.plugin.file_importer import FileImporter
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.service import PluginRequest

# Note: this aligns with the same document in the internal Engine test.
HANDLE = "test-importer-plugin-v1"
TEST_H1 = "A Poem"
TEST_S1 = "Roses are red."
TEST_S2 = "Violets are blue."
TEST_S3 = "Sugar is sweet, and I love you."
TEST_DOC = f"# {TEST_H1}\n\n{TEST_S1} {TEST_S2}\n\n{TEST_S3}\n"


class TestFileImporterPlugin(FileImporter, App):
    def run(
        self, request: PluginRequest[FileImportPluginInput]
    ) -> Response[RawDataPluginOutput]:
        return Response(
            data=RawDataPluginOutput(
                string=TEST_DOC,
                mime_type=MimeTypes.MKD
            )
        )

    @post("import")
    def do_import(self, **kwargs) -> Any:
        # TODO (enias): Move this code up one abstraction level
        import_request = FileImporter.parse_request(request=kwargs)
        return self.run(import_request)


handler = create_handler(TestFileImporterPlugin)
