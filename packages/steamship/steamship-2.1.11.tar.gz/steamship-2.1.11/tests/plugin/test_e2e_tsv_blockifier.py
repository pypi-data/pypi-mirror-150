from .. import APPS_PATH

__copyright__ = "Steamship"
__license__ = "MIT"

from ..utils.client import get_steamship_client
from ..utils.deployables import deploy_plugin
from ..utils.file import upload_file


def test_e2e_tsv_blockifier_plugin():
    csv_blockifier_plugin_path = (
        APPS_PATH / "plugins" / "blockifiers" / "tsv_blockifier.py"
    )
    client = get_steamship_client()

    version_config_template = dict(
        text_column=dict(type="string"),
        tag_columns=dict(type="string"),
        tag_kind=dict(type="string"),
    )
    instance_config = dict(  # Has to match up
        text_column="Message",
        tag_columns="Category",
        tag_kind="Intent",
    )
    with deploy_plugin(
        client,
        csv_blockifier_plugin_path,
        "blockifier",
        version_config_template=version_config_template,
        instance_config=instance_config,
    ) as (plugin, version, instance):
        with upload_file(client, "utterances.tsv") as file:
            assert len(file.refresh().data.blocks) == 0
            file.blockify(plugin_instance=instance.handle).wait()
            # Check the number of blocks
            blocks = file.refresh().data.blocks
            assert len(blocks) == 5
            # Check if the tags are correctly added
            for block in blocks:
                assert block.tags is not None
                assert len(block.tags) > 0
                for tag in block.tags:
                    assert tag.name is not None
                    assert tag.kind is not None
            file.delete()
