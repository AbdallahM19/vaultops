"""Hardware Module"""

from dataclasses import dataclass

from vaultops.models.base import BaseEntry


@dataclass
class HardwareItem(BaseEntry):
    device_name: str
    serial_number: str
    quantity: int

