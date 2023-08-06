from typing import Optional, Any, Dict
from dataclasses import dataclass
from ..enums import *
from .simple_option import SimpleOption


@dataclass
class Position:
    option: SimpleOption
    position: float
    average_entry_price: float
    mark_price: Optional[float]

    @classmethod
    def from_data(cls, data):
        """Create an Position instance from the provided data dictionary."""
        option = SimpleOption.from_data(data["option"])
        position = float(data["position"])
        average_entry_price = (
            float(data["average_entry_price"]) if data["average_entry_price"] else None
        )
        mark_price = float(data["mark_price"]) if data["mark_price"] else None

        return Position(
            option=option,
            position=position,
            average_entry_price=average_entry_price,
            mark_price=mark_price,
        )
