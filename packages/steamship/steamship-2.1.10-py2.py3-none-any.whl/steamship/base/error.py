import logging
from dataclasses import dataclass
from typing import Any, Union


@dataclass
class SteamshipError(Exception):
    message: str = None
    internalMessage: str = None
    suggestion: str = None
    code: str = None
    error: str = None

    def __init__(
        self,
        message: str = "Undefined remote error",
        internal_message: str = None,
        suggestion: str = None,
        code: str = None,
        error: Union[Exception, str] = None,
    ):
        self.message = message
        self.suggestion = suggestion
        self.internalMessage = internal_message
        self.statusCode = code
        if error is not None:
            self.error = str(error)

        parts = []
        if code is not None:
            parts.append(f"[{code}]")
        if message is not None:
            parts.append(message)
        if internal_message is not None:
            parts.append(f"Internal Message: {internal_message}")
        if suggestion is not None:
            parts.append(f"Suggestion: {suggestion}")

        super().__init__("\n".join(parts))

    def log(self):
        logging.error(
            f"[{self.code}] {self.message}. [Internal: {self.internalMessage}] [Suggestion: { self.suggestion}]"
        )
        if self.error:
            logging.error(self.error)

    def to_dict(self) -> dict:
        return dict(
            message=self.message,
            internalMessage=self.internalMessage,
            suggestion=self.suggestion,
            code=self.code,
            error=self.error,
        )

    @staticmethod
    def from_dict(d: Any) -> "SteamshipError":
        """Last resort if subclass doesn't override: pass through."""
        return SteamshipError(
            message=d.get("statusMessage", d.get("message", None)),
            internal_message=d.get("internalMessage", None),
            suggestion=d.get("statusSuggestion", d.get("suggestion", None)),
            code=d.get("statusCode", d.get("code", None)),
            error=d.get("error", d.get("error", None)),
        )
