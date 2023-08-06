from dataclasses import dataclass
from typing import Any, Dict

from steamship.base import Client, Request
from steamship.base.response import Response
from steamship.plugin.inputs.export_plugin_input import ExportPluginInput
from steamship.plugin.inputs.training_parameter_plugin_input import (
    TrainingParameterPluginInput,
)
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.outputs.training_parameter_plugin_output import (
    TrainingParameterPluginOutput,
)


class PluginInstance:
    pass


@dataclass
class CreatePluginInstanceRequest(Request):
    id: str = None
    pluginId: str = None
    pluginHandle: str = None
    pluginVersionId: str = None
    pluginVersionHandle: str = None
    handle: str = None
    upsert: bool = None
    config: Dict[str, Any] = None


@dataclass
class DeletePluginInstanceRequest(Request):
    id: str


@dataclass
class PluginInstance:
    client: Client = None
    id: str = None
    handle: str = None
    plugin_id: str = None
    plugin_version_id: str = None
    user_id: str = None
    config: Dict[str, Any] = None
    spaceId: str = None

    @staticmethod
    def from_dict(d: Any, client: Client = None) -> "PluginInstance":
        if "pluginInstance" in d:
            d = d["pluginInstance"]

        return PluginInstance(
            client=client,
            id=d.get("id", None),
            handle=d.get("handle", None),
            plugin_id=d.get("pluginId", None),
            plugin_version_id=d.get("pluginVersionId", None),
            config=d.get("config", None),
            user_id=d.get("userId", None),
        )

    @staticmethod
    def create(
        client: Client,
        plugin_id: str = None,
        plugin_handle: str = None,
        plugin_version_id: str = None,
        plugin_version_handle: str = None,
        handle: str = None,
        upsert: bool = None,
        config: Dict[str, Any] = None,
    ) -> Response[PluginInstance]:
        req = CreatePluginInstanceRequest(
            handle=handle,
            pluginId=plugin_id,
            pluginHandle=plugin_handle,
            pluginVersionId=plugin_version_id,
            pluginVersionHandle=plugin_version_handle,
            upsert=upsert,
            config=config,
        )

        return client.post("plugin/instance/create", payload=req, expect=PluginInstance)

    def delete(self) -> PluginInstance:
        req = DeletePluginInstanceRequest(id=self.id)
        return self.client.post(
            "plugin/instance/delete", payload=req, expect=PluginInstance
        )

    def export(self, input: ExportPluginInput) -> Response[RawDataPluginOutput]:
        input.pluginInstance = self.handle
        return self.client.post(
            "plugin/instance/export", payload=input, expect=RawDataPluginOutput
        )

    def train(self, training_request: TrainingParameterPluginInput) -> PluginInstance:
        return self.client.post(
            "plugin/instance/train", payload=training_request, expect=PluginInstance
        )

    def get_training_parameters(
        self, training_request: TrainingParameterPluginInput
    ) -> PluginInstance:
        return self.client.post(
            "plugin/instance/getTrainingParameters",
            payload=training_request,
            expect=TrainingParameterPluginOutput,
        )


@dataclass
class ListPrivatePluginInstancesRequest(Request):
    pass
