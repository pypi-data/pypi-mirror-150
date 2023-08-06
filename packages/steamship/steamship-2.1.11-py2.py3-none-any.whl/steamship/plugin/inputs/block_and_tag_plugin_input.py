from dataclasses import dataclass
from typing import Any, Dict, Optional

from steamship import File
from steamship.base import Client


@dataclass
class BlockAndTagPluginInput:
    file: File = None

    @staticmethod
    def from_dict(
        d: Any = None, client: Client = None
    ) -> "Optional[BlockAndTagPluginInput]":
        if d is None:
            return None

        return BlockAndTagPluginInput(
            file=File.from_dict(d.get("file", None), client=client)
        )

    def to_dict(self) -> Dict:
        if self.file is None:
            return {}
        return dict(file=self.file.to_dict())
