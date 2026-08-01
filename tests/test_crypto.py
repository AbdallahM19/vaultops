"""test crypto"""

import pytest

from vaultops.exceptions import SecurityError
from vaultops.security.crypto import generate_key, encrypt, decrypt


def test_encrypt_decrypt_roundtrip():
    key = generate_key()

    password = decrypt(encrypt("hunter22", key), key)
    assert password == "hunter22"

def test_decrypt_wrong_key_raises():
    key = generate_key()

    encryption = encrypt("hunter22", key)

    with pytest.raises(SecurityError) as exc_error:
        decrypt(encryption, generate_key())

    assert "wrong key" in str(exc_error.value)

def test_encrypt_output_differs_from_plaintext():
    key = generate_key()

    encryption = encrypt("hunter22", key)

    assert encryption != "hunter22"
