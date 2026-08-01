"""test cli"""

import pytest

from datetime import datetime
from vaultops.cli import handle_list
from types import SimpleNamespace
from vaultops.models.credential import Credential
from vaultops.storage.json_storage import StorageSession, JsonCredentialStorage


def test_handle_list_empty_logs_no_credentials(tmp_path, caplog):
    file_path = tmp_path / "creds.json"
    key_path = tmp_path / "vault.key"

    file_path.write_text("[]")

    with caplog.at_level("INFO"):
        handle_list(
            SimpleNamespace(service = None),
            file_path, key_path
        )

    assert "No credentials stored." in caplog.text

def test_handle_list_with_service_filter(tmp_path, caplog):
    file_path = tmp_path / "creds.json"
    key_path = tmp_path / "vault.key"
    entry = [
        Credential(
            service_name="aws",
            created_at=datetime.now(),
            entry_id="cred-001",
            username="ali",
            password="hunter22"
        ),
        Credential(
            service_name="github",
            created_at=datetime.now(),
            entry_id="cred-002",
            username="wolv",
            password="wolv@2150"
        )
    ]

    with StorageSession(file_path, key_path) as store:
        for i in entry:
            store.save(i)
            with open(file_path) as f:
                print(f.read())

    with caplog.at_level("INFO"):
        handle_list(
            SimpleNamespace(service = "aws"),
            file_path, key_path
        )

    assert 'Running command:' in caplog.records[0].message
    assert all(
        "aws" in i.message
        for i in caplog.records[1:-1]
    )
    assert 'Finished command:' in caplog.records[-1].message

