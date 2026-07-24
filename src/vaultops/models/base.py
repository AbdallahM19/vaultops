"""Base Module"""

from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class BaseEntry:
    entry_id: str
    created_at: datetime
    tags: list[str] = field(default_factory = list)

