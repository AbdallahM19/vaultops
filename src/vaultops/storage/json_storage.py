"""json storage module"""

import json

from datetime import datetime
from dataclasses import asdict
from vaultops.models.credential import Credential
from vaultops.exceptions import DuplicateEntryError, EntryNotFoundError, StorageError


class JsonCredentialStorage:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def _serialize(self, data: list[Credential]) -> None:
        creds_to_dict = []

        for x in data:
            i = asdict(x)
            i['created_at'] = x.created_at.isoformat()
            creds_to_dict.append(i)

        with open(self.file_path, "w") as f:
            json.dump(creds_to_dict, f, indent = 4)

    def list_all(self) -> list[Credential]:
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise StorageError("The storage file not found.")
        except json.JSONDecodeError:
            raise StorageError("Failed to parse JSON storage file.")

        creds = []

        for i in data:
            x = i.copy()
            x['created_at'] = datetime.fromisoformat(i['created_at'])
            creds.append(Credential(**x))

        return creds

    def get(self, entry_id: str) -> Credential:
        data = self.list_all()

        for i in data:
            if i.entry_id == entry_id:
                return i

        raise EntryNotFoundError(f"entry_id '{entry_id}' not found")

    def save(self, entry: Credential) -> None:
        data = self.list_all()

        for i in data:
            if i.entry_id == entry.entry_id:
                raise DuplicateEntryError(f"entry_id '{entry.entry_id}' already exists")

        data.append(entry)

        self._serialize(data)

    def delete(self, entry_id: str) -> None:
        is_exists = False
        entry_idx = 0
        data = self.list_all()

        for i, x in enumerate(data):
            if x.entry_id == entry_id:
                is_exists = True
                entry_idx = i
                break

        if not is_exists:
            raise EntryNotFoundError(f"entry_id '{entry_id}' not found")

        data.pop(entry_idx)

        self._serialize(data)

