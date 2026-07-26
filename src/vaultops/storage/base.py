"""Storage Module"""

from typing import Protocol, runtime_checkable

from vaultops.models.base import BaseEntry


@runtime_checkable
class EntryStorage(Protocol):
    """a structural interface that concrete storage backends"""
    def save(self, entry: BaseEntry) -> None: ...
    def get(self, entry_id: str) -> BaseEntry: ...
    def delete(self, entry_id: str) -> None: ...
    def list_all(self) -> list[BaseEntry]: ...

