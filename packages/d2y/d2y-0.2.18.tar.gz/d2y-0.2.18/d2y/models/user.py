from typing import Optional, Any, Dict
from enum import Enum
from dataclasses import dataclass


@dataclass
class UserBalance:
    asset: str
    free_balance: str
    locked_balance: str

    @classmethod
    def from_data(cls, data):
        """Create a UserBalance instance from the provided data dictionary."""
        return UserBalance(
            asset=data["asset"],
            free_balance=data["free_balance"],
            locked_balance=data["locked_balance"],
        )


@dataclass
class UserProfile:
    @classmethod
    def from_data(cls, data):
        return UserProfile()


@dataclass
class User:
    """Represents a user with balances and profile information."""

    balances: list[UserBalance]
    profile: UserProfile
    equity: float
    wallet_address: str

    @classmethod
    def from_data(cls, data):
        """Create a User instance from the provided data dictionary."""
        balances = data.get("balances", [])
        profile = data.get("profile", {})
        equity = data.get("equity", 0)
        wallet_address = data.get("wallet_address", "")

        return User(
            balances=balances,
            profile=profile,
            equity=equity,
            wallet_address=wallet_address,
        )
