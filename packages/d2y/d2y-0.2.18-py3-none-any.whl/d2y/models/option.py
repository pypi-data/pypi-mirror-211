from typing import Optional, Any, Dict
from dataclasses import dataclass
from .order import Order
from ..enums import *


@dataclass
class Option:
    id: int
    best_bid: Order
    best_ask: Order
    open_interest: float
    implied_volatility_bids: float
    implied_volatility_asks: float
    delta: float
    vega: float
    gamma: float
    rho: float
    theta: float
    strike_price: float
    expiration_timestamp: str
    option_type: OptionType
    settlement_period: SettlementPeriodType
    underlying_price_at_expiration: str
    mark_price: Optional[float]
    mark_price_updated_at: Optional[str]
    asset: str
    created_at: Optional[str]
    instrument_name: str
    mark_price_iv: Optional[float]

    @classmethod
    def from_data(cls, data):
        """Create an Option instance from the provided data dictionary."""
        best_bid = (
            Order.from_data(data.get("best_bid", None))
            if data.get("best_bid", None)
            else None
        )
        best_ask = (
            Order.from_data(data.get("best_ask", None))
            if data.get("best_ask", None)
            else None
        )
        open_interest = float(data.get("open_interest", 0))
        implied_volatility_bids = float(data.get("implied_volatility_bids", 0))
        implied_volatility_asks = float(data.get("implied_volatility_asks", 0))
        delta = float(data.get("delta", 0))
        vega = float(data.get("vega", 0))
        gamma = float(data.get("gamma", 0))
        rho = float(data.get("rho", 0))
        theta = float(data.get("theta", 0))
        strike_price = float(data.get("strike_price", 0))
        expiration_timestamp = data.get("expiration_timestamp", "")
        option_type = OptionType(data.get("option_type", OptionType.CALL))
        settlement_period = SettlementPeriodType(
            data.get("settlement_period", SettlementPeriodType.OTHER)
        )
        underlying_price_at_expiration = data.get("underlying_price_at_expiration", "")
        mark_price = float(data.get("mark_price")) if data.get("mark_price") else None
        mark_price_updated_at = (
            data.get("mark_price_updated_at", "")
            if data.get("mark_price_updated_at")
            else None
        )
        asset = data.get("asset", "")
        created_at = data.get("created_at", "")
        instrument_name = data.get("instrument_name", "")
        mark_price_iv = (
            float(data.get("mark_price_iv")) if data.get("mark_price_iv") else None
        )
        id = int(data["id"])

        return Option(
            best_bid=best_bid,
            best_ask=best_ask,
            open_interest=open_interest,
            implied_volatility_bids=implied_volatility_bids,
            implied_volatility_asks=implied_volatility_asks,
            delta=delta,
            vega=vega,
            gamma=gamma,
            rho=rho,
            theta=theta,
            strike_price=strike_price,
            expiration_timestamp=expiration_timestamp,
            option_type=option_type,
            settlement_period=settlement_period,
            underlying_price_at_expiration=underlying_price_at_expiration,
            mark_price=mark_price,
            mark_price_updated_at=mark_price_updated_at,
            asset=asset,
            created_at=created_at,
            instrument_name=instrument_name,
            mark_price_iv=mark_price_iv,
            id=id,
        )
