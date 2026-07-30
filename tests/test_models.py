"""test module"""

import pytest

from datetime import datetime
from vaultops.exceptions import ValidationError
from vaultops.models.base import BaseEntry
from vaultops.models.hardware import HardwareItem
from vaultops.models.credential import Credential


def test_base_entry_valid_construction():
    entry_id = "id-01"
    created_at = datetime.now()

    base_entry = BaseEntry(
        entry_id=entry_id,
        created_at=created_at
    )

    assert base_entry.entry_id == entry_id
    assert base_entry.display_id == f"[{entry_id}]"

def test_base_entry_empty_entry_id_raises():
    entry_id = ""
    created_at = datetime.now()

    with pytest.raises(ValidationError) as error_exp:
        BaseEntry(entry_id=entry_id, created_at=created_at)

    assert 'a non-empty string' in str(error_exp.value)

def test_credential_short_password_raises():
    entry_id='cred-001'
    created_at=datetime.now()
    service_name='github'
    username='gazy'
    password='hun'

    with pytest.raises(ValidationError) as error_exp:
        Credential(
            entry_id=entry_id, created_at=created_at,
            service_name=service_name, username=username,
            password=password
        )

    assert 'at least 8' in str(error_exp.value)

def test_credential_display_id():
    entry_id='cred-001'
    created_at=datetime.now()
    service_name='github'
    username='gazy'
    password='hunter-001'

    cred_entry = Credential(
        entry_id=entry_id, created_at=created_at,
        service_name=service_name, username=username,
        password=password
    )

    assert cred_entry.display_id == f"[{entry_id}]"

def test_hardware_item_invalid_quantity_raises():
    with pytest.raises(ValidationError) as error_exp:
        HardwareItem(
            entry_id="cred-001",
            created_at=datetime.now(),
            device_name="RAM",
            serial_number="RAM-001",
            quantity=0
        )

    assert 'at least 1' in str(error_exp.value)

def test_hardware_item_valid_construction():
    item_dict = {
        'entry_id': "cred-001",
        'created_at': datetime.now(),
        'device_name': "RAM",
        'serial_number': "RAM-001",
        'quantity': 2
    }

    hardware_item = HardwareItem(**item_dict)

    assert item_dict['quantity'] == hardware_item.quantity
    assert hardware_item.display_id == f'[{item_dict["entry_id"]}]'
    assert item_dict['serial_number'] == hardware_item.serial_number
    assert item_dict['device_name'] == hardware_item.device_name

