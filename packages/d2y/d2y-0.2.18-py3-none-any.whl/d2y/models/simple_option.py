from typing import Optional, Any, Dict
from dataclasses import dataclass
from ..enums import *


@dataclass
class SimpleOption:
    id: int
    strike_price: float
    expiration_timestamp: str
    option_type: OptionType
    asset: str

    @classmethod
    def from_data(cls, data):
        """Create an SimpleOrder instance from the provided data dictionary."""
        id = float(data.get("id", 0))
        strike_price = float(data.get("strike_price", 0))
        expiration_timestamp = data.get("expiration_timestamp", "")
        option_type = OptionType(data.get("option_type", OptionType.CALL))
        asset = data.get("asset", "")

        return SimpleOption(
            id=id,
            strike_price=strike_price,
            expiration_timestamp=expiration_timestamp,
            option_type=option_type,
            asset=asset,
        )
