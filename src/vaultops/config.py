"""Config module"""

import os
import json

from vaultops.security.crypto import generate_key

KEY_PATH: str = "data/vault.key"
FILE_PATH: str = "data/credentials.json"


def get_or_create_key(path: str) -> bytes:
    if os.path.exists(path):
        with open(path, "rb") as f:
            key = f.read()
    else:
        key = generate_key()
        with open(path, "wb") as f:
            f.write(key)
    return key

def get_or_create_credentials_file(path: str) -> None:
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)


