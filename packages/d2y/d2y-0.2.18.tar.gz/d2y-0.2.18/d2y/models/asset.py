from typing import Optional, Any, Dict
from dataclasses import dataclass


@dataclass
class Asset:
    """Represents an asset with its associated information."""

    total_open_interest: float
    notional_volume_24h: float
    expiration_timestamps: list[str]
    name: str
    ticker: str
    underlying_price: Optional[float]
    underlying_price_updated_at: Optional[str]

    @classmethod
    def from_data(cls, data):
        """Create an Asset instance from the provided data dictionary."""
        total_open_interest = float(data.get("total_open_interest", 0))
        notional_volume_24h = float(data.get("notional_volume_24h", 0))
        expiration_timestamps = data.get("expiration_timestamps", [])
        name = data.get("name", "")
        ticker = data.get("ticker", "")
        underlying_price = data.get("underlying_price", None)
        underlying_price_updated_at = data.get("underlying_price_updated_at", None)

        return Asset(
            total_open_interest=total_open_interest,
            notional_volume_24h=notional_volume_24h,
            expiration_timestamps=expiration_timestamps,
            name=name,
            ticker=ticker,
            underlying_price=underlying_price,
            underlying_price_updated_at=underlying_price_updated_at,
        )
