"""User entity for domain data and rules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    """Represents a user in the domain layer.

    Attributes:
        user_id: Unique numeric identifier for a user.
        name: Display name of the user.
        email: Email address of the user.
    """

    user_id: int
    name: str
    email: str

    def __post_init__(self) -> None:
        """Validate invariants after initialization."""
        self._validate_user_id(self.user_id)
        self._validate_name(self.name)
        self._validate_email(self.email)

    def rename(self, new_name: str) -> User:
        """Return a new user with an updated name.

        Args:
            new_name: New display name to set.

        Returns:
            A new User instance with the updated name.
        """
        self._validate_name(new_name)
        return User(user_id=self.user_id, name=new_name, email=self.email)

    def change_email(self, new_email: str) -> User:
        """Return a new user with an updated email.

        Args:
            new_email: New email address to set.

        Returns:
            A new User instance with the updated email.
        """
        self._validate_email(new_email)
        return User(user_id=self.user_id, name=self.name, email=new_email)

    @staticmethod
    def _validate_user_id(user_id: int) -> None:
        """Validate user identifier.

        Args:
            user_id: Value to validate.

        Raises:
            ValueError: If user_id is not a positive integer.
        """
        if user_id <= 0:
            raise ValueError("user_id must be a positive integer")

    @staticmethod
    def _validate_name(name: str) -> None:
        """Validate user name.

        Args:
            name: Value to validate.

        Raises:
            ValueError: If name is empty after stripping.
        """
        if not name.strip():
            raise ValueError("name must not be blank")

    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format with lightweight checks.

        Args:
            email: Value to validate.

        Raises:
            ValueError: If email does not include basic required tokens.
        """
        if "@" not in email:
            raise ValueError("email format is invalid")

        local, domain = email.split("@", maxsplit=1)
        if not local or "." not in domain:
            raise ValueError("email format is invalid")
