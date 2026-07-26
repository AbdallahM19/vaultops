"""Hardware Module"""

from dataclasses import dataclass

from vaultops.exceptions import ValidationError
from vaultops.models.base import BaseEntry


@dataclass
class HardwareItem(BaseEntry):
    device_name: str
    serial_number: str
    quantity: int

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.device_name == "":
            raise ValidationError("device_name must be a non-empty string")

        if self.serial_number == "":
            raise ValidationError("serial_number must be a non-empty string")

        if self.quantity <= 0:
            raise ValidationError("quantity must be at least 1")
