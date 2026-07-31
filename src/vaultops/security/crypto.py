"""security module"""

from cryptography.fernet import Fernet, InvalidToken
from vaultops.exceptions import SecurityError


def generate_key() -> bytes:
    return Fernet.generate_key()

def encrypt(plaintext: str, key: bytes) -> str:
    try:
        f = Fernet(key)

        plaintext_encoded = plaintext.encode("utf-8")
        data_encrypted = f.encrypt(plaintext_encoded)
        data_encrypted_decoded = data_encrypted.decode("utf-8")

        return data_encrypted_decoded
    except ValueError as e:
        raise SecurityError(f"Value-Error: {e}") from e

def decrypt(token: str, key: bytes) -> str:
    try:
        f = Fernet(key)

        decrypts = token.encode("utf-8")
        decrypt_data = f.decrypt(decrypts)
        decrypt_data_decoded = decrypt_data.decode("utf-8")

        return decrypt_data_decoded
    except InvalidToken:
        raise SecurityError("Invalid token or wrong key")

