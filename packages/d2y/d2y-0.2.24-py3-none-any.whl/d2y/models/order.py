from typing import Optional, Any, Dict
from dataclasses import dataclass
from ..enums import *
from .simple_option import SimpleOption


@dataclass
class Order:
    id: int
    option: SimpleOption
    average_price_matched: Optional[float]
    price: Optional[float]
    quantity: float
    quantity_filled: float
    side: OrderSide
    created_at: str
    status: OrderStatus
    locked_collateral: float
    order_type: OrderType
    user: int

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Order":
        """Create an Order instance from the provided data dictionary."""
        return cls(
            id=data["id"],
            option=SimpleOption.from_data(data["option"]),
            average_price_matched=float(data["average_price_matched"])
            if data["average_price_matched"]
            else None,
            price=float(data["price"]) if data["price"] else None,
            quantity=float(data["quantity"]),
            quantity_filled=float(data["quantity_filled"]),
            side=OrderSide(data["side"]),
            created_at=data["created_at"],
            status=OrderStatus(data["status"]),
            locked_collateral=float(data["locked_collateral"]),
            order_type=OrderType(data["order_type"]),
            user=data["user"],
        )


@dataclass
class PlaceOrderArgs:
    option: int
    quantity: float
    side: OrderSide
    order_type: OrderType
    price: Optional[float] = None
