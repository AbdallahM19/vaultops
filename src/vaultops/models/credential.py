"""Credential module"""

from dataclasses import dataclass

from vaultops.models.base import BaseEntry


@dataclass
class Credential(BaseEntry):
    service_name: str
    username: str
    password: str

