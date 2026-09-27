"""Unit tests for security module"""

import pytest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_not_expired,
)


class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_hash_password(self):
        """Test password hashing"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 20

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False


class TestJWTTokens:
    """Test JWT token generation and validation"""

    def test_create_access_token(self):
        """Test creating access token"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20

    def test_create_refresh_token(self):
        """Test creating refresh token"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20

    def test_decode_access_token(self):
        """Test decoding valid access token"""
        user_id = 123
        email = "test@example.com"
        data = {"sub": email, "user_id": user_id}
        token = create_access_token(data)

        decoded = decode_token(token)

        assert decoded is not None
        assert decoded["sub"] == email
        assert decoded["user_id"] == user_id

    def test_decode_invalid_token(self):
        """Test decoding invalid token"""
        invalid_token = "invalid.token.here"
        decoded = decode_token(invalid_token)

        assert decoded is None

    def test_token_not_expired(self):
        """Test that fresh token is not expired"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert verify_token_not_expired(token) is True

    def test_verify_refresh_token_type(self):
        """Test that refresh token has correct type"""
        data = {"sub": "test@example.com"}
        token = create_refresh_token(data)
        decoded = decode_token(token)

        assert decoded is not None
        assert decoded.get("type") == "refresh"
