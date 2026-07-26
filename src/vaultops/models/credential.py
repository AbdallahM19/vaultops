"""Credential module"""

from dataclasses import dataclass

from vaultops.exceptions import ValidationError
from vaultops.models.base import BaseEntry


@dataclass
class Credential(BaseEntry):
    service_name: str
    username: str
    password: str

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.service_name == "":
            raise ValidationError("service_name must be a non-empty string")

        if self.username == "":
            raise ValidationError("username must be a non-empty string")

        if len(self.password) < 8:
            raise ValidationError("password must be at least 8 characters")
