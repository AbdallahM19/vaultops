"""unit test for storage"""

import pytest

from datetime import datetime
from vaultops.models.credential import Credential
from vaultops.exceptions import DuplicateEntryError, EntryNotFoundError, StorageError
from vaultops.storage.json_storage import JsonCredentialStorage


def make_storage(tmp_path) -> JsonCredentialStorage:
    path = tmp_path / "creds.json"
    path.write_text("[]")

    return JsonCredentialStorage(str(path))

def test_save_then_list_all(tmp_path):
    json_cred = make_storage(tmp_path)
    entry = Credential(
        entry_id = "cred-002",
        created_at = datetime.now(),
        tags = [],
        service_name = "github",
        username = "ghub",
        password = "git20@04"
    )
    json_cred.save(entry)

    creds = json_cred.list_all()
    assert len(creds) == 1
    assert creds[0] == entry

def test_save_duplicate_raises(tmp_path):
    json_cred = make_storage(tmp_path)
    entry = Credential(
        entry_id = "cred-002",
        created_at = datetime.now(),
        tags = [],
        service_name = "github",
        username = "ghub",
        password = "git20@04"
    )
    json_cred.save(entry)

    with pytest.raises(DuplicateEntryError) as error_exp:
        json_cred.save(entry)
    assert 'already exists' in str(error_exp.value)

def test_get_missing_raises(tmp_path):
    json_cred = make_storage(tmp_path)
    entry = Credential(
        entry_id = "cred-002",
        created_at = datetime.now(),
        tags = [],
        service_name = "github",
        username = "ghub",
        password = "git20@04"
    )

    with pytest.raises(EntryNotFoundError) as error_exp:
        json_cred.get(entry.entry_id)
    assert 'not found' in str(error_exp.value)

def test_delete_then_redelete_raises(tmp_path):
    json_cred = make_storage(tmp_path)
    entry = Credential(
        entry_id = "cred-002",
        created_at = datetime.now(),
        tags = [],
        service_name = "github",
        username = "ghub",
        password = "git20@04"
    )
    json_cred.save(entry)

    json_cred.delete(entry.entry_id)

    with pytest.raises(EntryNotFoundError) as error_exp:
        json_cred.delete(entry.entry_id)

    assert 'not found' in str(error_exp.value)

def test_list_all_missing_file_raises():
    json_cred = JsonCredentialStorage("fake/data.json")

    with pytest.raises(StorageError) as error_exp:
        json_cred.list_all()

    assert 'not found' in str(error_exp.value)

