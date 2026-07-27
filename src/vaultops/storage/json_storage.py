"""json storage module"""

import json

from datetime import datetime
from vaultops.models.credential import Credential
from vaultops.exceptions import EntryNotFoundError, StorageError

class JsonCredentialStorage:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

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

