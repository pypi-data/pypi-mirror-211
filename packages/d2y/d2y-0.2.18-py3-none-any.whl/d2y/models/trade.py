from typing import Optional, Any, Dict
from dataclasses import dataclass
from ..enums import *
from .simple_option import SimpleOption


@dataclass
class Trade:
    created_at: str
    option: SimpleOption
    price: float
    quantity: float
    order_type: OrderType
    order_side: OrderSide
    pnl: float
    fees: float
    is_maker: bool

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Trade":
        """Create a Trade instance from the provided data dictionary."""
        return Trade(
            created_at=data["created_at"],
            option=SimpleOption.from_data(data["option"]),
            price=float(data["price"]),
            quantity=float(data["quantity"]),
            order_type=OrderType(data["order_type"]),
            order_side=OrderSide(data["order_side"]),
            pnl=float(data["pnl"]),
            fees=float(data["fees"]),
            is_maker=data["is_maker"],
        )
