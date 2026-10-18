"""Time-based one-time passwords (RFC 6238) for two-factor authentication.

Codes are HMAC-SHA1 over the current 30-second counter, truncated to six digits. Verification
accepts the previous and next step as well, to absorb small clock drift between the server and
the authenticator app.
"""

import base64
import hashlib
import hmac
import secrets
import struct
import time
from urllib.parse import quote

STEP_SECONDS = 30
DIGITS = 6
ISSUER = "AetherCMS AI"


def generate_secret() -> str:
    """A new random 160-bit secret, base32-encoded the way authenticator apps expect."""
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def _key(secret: str) -> bytes:
    padded = secret.upper() + "=" * (-len(secret) % 8)
    return base64.b32decode(padded)


def code_at(secret: str, timestamp: float, digits: int = DIGITS) -> str:
    """The code valid at ``timestamp`` (seconds since the epoch)."""
    counter = int(timestamp // STEP_SECONDS)
    digest = hmac.new(_key(secret), struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    value = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(value % (10 ** digits)).zfill(digits)


def verify_code(secret: str, code: str, now: float = None, window: int = 1) -> bool:
    """True when ``code`` matches the secret at this step or within ``window`` steps either side."""
    if not secret or not code or not code.isdigit() or len(code) != DIGITS:
        return False
    current = time.time() if now is None else now
    matched = False
    for offset in range(-window, window + 1):
        candidate = code_at(secret, current + offset * STEP_SECONDS)
        matched = hmac.compare_digest(candidate, code) or matched
    return matched


def provisioning_uri(secret: str, account: str) -> str:
    """The otpauth:// URI an authenticator app reads (usually shown as a QR code)."""
    label = quote(f"{ISSUER}:{account}")
    return f"otpauth://totp/{label}?secret={secret}&issuer={quote(ISSUER)}&digits={DIGITS}&period={STEP_SECONDS}"
