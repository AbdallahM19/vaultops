"""Base Module"""

from datetime import datetime
from dataclasses import dataclass, field

from vaultops.exceptions import ValidationError


@dataclass
class BaseEntry:
    entry_id: str
    created_at: datetime
    tags: list[str] = field(
            default_factory = list,
            kw_only = True
    )

    def __post_init__(self) -> None:
        if self.entry_id == "":
            raise ValidationError("entry_id must be a non-empty string")
        if not isinstance(self.entry_id, str):
            raise ValidationError("entry_id must be a str")

    @property
    def display_id(self) -> str:
        return f"[{self.entry_id}]"

