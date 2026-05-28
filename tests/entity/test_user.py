"""Tests for the User entity."""

import pytest

from src.entity.user import User


def test_create_user_with_valid_values() -> None:
    """Create User when all values are valid."""
    # Arrange
    user_id = 1
    name = "Alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, name=name, email=email)

    # Assert
    assert user.user_id == user_id
    assert user.name == name
    assert user.email == email


def test_raise_error_when_name_is_blank() -> None:
    """Raise ValueError when name is blank."""
    # Arrange
    user_id = 1
    name = "   "
    email = "alice@example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="name must not be blank"):
        User(user_id=user_id, name=name, email=email)


def test_raise_error_when_email_is_invalid() -> None:
    """Raise ValueError when email format is invalid."""
    # Arrange
    user_id = 1
    name = "Alice"
    email = "alice-at-example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="email format is invalid"):
        User(user_id=user_id, name=name, email=email)


def test_rename_returns_new_user() -> None:
    """Return a new User with updated name."""
    # Arrange
    original = User(user_id=1, name="Alice", email="alice@example.com")
    new_name = "Alicia"

    # Act
    renamed = original.rename(new_name)

    # Assert
    assert renamed is not original
    assert renamed.name == new_name
    assert renamed.email == original.email
    assert renamed.user_id == original.user_id


def test_change_email_returns_new_user() -> None:
    """Return a new User with updated email."""
    # Arrange
    original = User(user_id=1, name="Alice", email="alice@example.com")
    new_email = "alice.new@example.com"

    # Act
    updated = original.change_email(new_email)

    # Assert
    assert updated is not original
    assert updated.email == new_email
    assert updated.name == original.name
    assert updated.user_id == original.user_id
