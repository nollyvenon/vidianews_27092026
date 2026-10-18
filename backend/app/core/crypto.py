"""Symmetric encryption for values the server must read back (webhook signing secrets, sign-in payloads).

Keys are derived from ``SECRET_KEY``. Rotating ``SECRET_KEY`` makes previously encrypted values
unreadable; those values must then be re-entered by their owners.
"""

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings


class DecryptionError(Exception):
    """A stored value cannot be decrypted with the current key."""


def _cipher() -> Fernet:
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest())
    return Fernet(key)


def encrypt_value(plain: str) -> str:
    return _cipher().encrypt(plain.encode()).decode()


def decrypt_value(ciphertext: str) -> str:
    try:
        return _cipher().decrypt(ciphertext.encode()).decode()
    except InvalidToken as exc:
        raise DecryptionError("Stored value cannot be decrypted with the current key") from exc
