"""json storage module"""

import json

from datetime import datetime
from dataclasses import asdict
from typing import Iterator
from vaultops.security.crypto import decrypt, encrypt
from vaultops.models.credential import Credential
from vaultops.exceptions import DuplicateEntryError, EntryNotFoundError, StorageError
from vaultops.config import get_or_create_credentials_file, get_or_create_key


class JsonCredentialStorage:
    def __init__(self, file_path: str, key: bytes) -> None:
        self.file_path = file_path
        self.key = key

    def _serialize(self, data: list[Credential]) -> None:
        creds_to_dict = []

        for x in data:
            i = asdict(x)
            i['created_at'] = x.created_at.isoformat()
            creds_to_dict.append(i)

        with open(self.file_path, "w") as f:
            json.dump(creds_to_dict, f, indent = 4)

    def list_all(self) -> list[Credential]:
        return list(self.export_all())

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

        entry_dict = vars(entry).copy()
        entry_dict.update(password = encrypt(entry.password, self.key))

        data.append(Credential(**entry_dict))

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

    def export_all(self) -> Iterator[Credential]:
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise StorageError("The storage file not found.")
        except json.JSONDecodeError:
            raise StorageError("Failed to parse JSON storage file.")

        for i in data:
            x = i.copy()
            x.update(
                created_at=datetime.fromisoformat(i['created_at']),
                password=decrypt(i['password'], self.key)
            )
            yield Credential(**x)



class StorageSession:
    def __init__(self, file_path: str, key_path: str) -> None:
        self.key_path = key_path
        self.file_path = file_path

    def __enter__(self) -> JsonCredentialStorage:
        get_or_create_credentials_file(self.file_path)
        key = get_or_create_key(self.key_path)

        return JsonCredentialStorage(self.file_path, key)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return None

