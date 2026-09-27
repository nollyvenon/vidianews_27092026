"""Authentication unit tests"""

import pytest
from datetime import datetime, timedelta, timezone
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.utils.exceptions import ValidationError


class TestPasswordHashing:
    """Test password hashing"""

    def test_hash_different_from_password(self):
        password = "TestPassword123!"
        hashed = hash_password(password)
        assert hashed != password

    def test_verify_correct_password(self):
        password = "TestPassword123!"
        hashed = hash_password(password)
        assert verify_password(password, hashed)

    def test_verify_wrong_password(self):
        password = "TestPassword123!"
        hashed = hash_password(password)
        assert not verify_password("WrongPassword", hashed)

    def test_hash_consistent_verification(self):
        password = "MySecurePassword123!"
        for _ in range(5):
            hashed = hash_password(password)
            assert verify_password(password, hashed)


class TestJWTTokens:
    """Test JWT token generation and validation"""

    def test_create_access_token(self):
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)
        assert token
        assert isinstance(token, str)
        assert len(token) > 20

    def test_create_refresh_token(self):
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)
        assert token
        assert isinstance(token, str)

    def test_decode_access_token(self):
        data = {"sub": "test@example.com", "user_id": 123}
        token = create_access_token(data)
        decoded = decode_token(token)

        assert decoded is not None
        assert decoded["sub"] == "test@example.com"
        assert decoded["user_id"] == 123

    def test_decode_invalid_token(self):
        decoded = decode_token("invalid.token.here")
        assert decoded is None

    def test_refresh_token_has_type(self):
        data = {"sub": "test@example.com"}
        token = create_refresh_token(data)
        decoded = decode_token(token)

        assert decoded is not None
        assert decoded.get("type") == "refresh"

    def test_token_expiry(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        decoded = decode_token(token)

        assert decoded is not None
        assert "exp" in decoded
        assert decoded["exp"] > datetime.now(timezone.utc).timestamp()
