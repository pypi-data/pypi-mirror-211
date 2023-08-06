import requests
from typing import Dict, Any, List, Optional

# from .models import Asset, CreateOrder, Option, Order, User
from .models import *
from .enums import *


class Error(Exception):
    pass


class AuthenticationError(Error):
    pass


class TradingClient:
    def __init__(self, api_key, api_secret, base_url="https://api.dev.d2y.exchange"):
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.user = None

    def _headers(self):
        return {"d2y-api-key": self.api_key, "d2y-api-secret": self.api_secret}

    def _get_data_from_response(self, url, params={}):
        try:
            response = requests.get(url, headers=self._headers(), params=params)
            response.raise_for_status()
            data = response.json()["data"]
            if isinstance(data, dict) and data.get("results"):
                return data["results"]
            else:
                return data
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.content} {str(e)}"
            )

    def _post_data_and_get_response(self, url, body={}):
        try:
            response = requests.post(url, headers=self._headers(), json=body)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.content} {str(e)}"
            )

    def get_user_info(self):
        """
        Get the information of the current user.

        :return: A User object containing the user's information.
        """
        url = f"{self.base_url}/accounts/me/"
        data = self._get_data_from_response(url)
        self.user = User.from_data(data)
        return self.user

    def get_assets(self) -> List[Asset]:
        """
        Get available assets.

        :return: A list of Asset objects.
        """
        url = f"{self.base_url}/options/assets"
        data = self._get_data_from_response(url)
        return [Asset.from_data(asset) for asset in data]

    def get_options(
        self,
        strike_price: list[float] = [],
        expiration_timestamp: list[str] = [],
        option_type: OptionType = None,
        ordering: str = None,
    ) -> List[Option]:
        """
        Get options based on the provided filters.

        :param strike_price: Filter options by strike price.
        :param expiration_timestamp: Filter options by expiration timestamp.
        :param option_type: Filter options by option type.
        :param ordering: Order the results by a specific field.
        :return: A list of Option objects.
        """
        url = f"{self.base_url}/options/options"
        params = {}

        if ordering:
            params["ordering"] = ordering
        if strike_price:
            params["strike_price"] = ",".join(map(str, strike_price))
        if expiration_timestamp:
            params["expiration_timestamp"] = ",".join(expiration_timestamp)
        if option_type:
            params["option_type"] = option_type

        data = self._get_data_from_response(url, params=params)
        return [Option.from_data(option) for option in data]

    def get_orderbook(self, option_id: int, depth: int = 10) -> Dict[str, Any]:
        """
        Get the orderbook for a specific option.

        :param option_id: The ID of the option.
        :return: A dictionary containing the orderbook data.
        """
        url = f"{self.base_url}/options/orderbook/{option_id}"
        params = {"depth": depth}
        data = self._get_data_from_response(url, params)
        return {
            "bids": [Order.from_data(order) for order in data["bids"]],
            "asks": [Order.from_data(order) for order in data["asks"]],
        }

    def get_orders(
        self,
        option_id: list[int] = [],
        status: list[OrderStatus] = [],
        ordering: str = None,
        limit: int = None,
        offset: int = None,
    ) -> List[Order]:
        """
        Get all option orders based on the provided filters.

        :param option_id: Filter orders by option IDs.
        :param status: Filter orders by status (Open, Closed, Canceled, etc.).
        :param ordering: Ordering of the results.
        :param limit: Limit the number of results.
        :param offset: Offset the results.
        :return: A list of dictionaries containing the option orders data.
        """
        url = f"{self.base_url}/options/orders"
        params = {}

        if option_id:
            params["option_id"] = ",".join(map(str, option_id))
        if status:
            params["status"] = ",".join(status)
        if ordering:
            params["ordering"] = ordering
        if limit is not None and offset is not None:
            params["limit"] = limit
            params["offset"] = offset

        data = self._get_data_from_response(url, params=params)
        return [Order.from_data(order) for order in data]

    def get_positions(self) -> List[Dict[str, Any]]:
        """
        Get the current user's option positions.

        :return: A list of dictionaries containing the option positions data.
        """
        url = f"{self.base_url}/options/positions"
        data = self._get_data_from_response(url)
        return [Position.from_data(position) for position in data]

    def get_trades(
        self,
        option_id: list[int] = [],
        option_type: list[OptionType] = [],
        option_strike_price: list[float] = [],
        option_expiration_timestamp: list[str] = [],
        limit: int = None,
        offset: int = None,
    ) -> List[Dict[str, Any]]:
        """
        Get the current user's option positions.

        :return: A list of dictionaries containing the option positions data.
        """
        url = f"{self.base_url}/options/trades"
        params = {}

        if option_id:
            params["option_id"] = ",".join(map(str, option_id))
        if option_type:
            params["option_type"] = ",".join(option_type)
        if option_strike_price:
            params["option_strike_price"] = ",".join(map(str, option_strike_price))
        if option_expiration_timestamp:
            params["option_expiration_timestamp"] = ",".join(
                option_expiration_timestamp
            )
        if limit is not None and offset is not None:
            params["limit"] = limit
            params["offset"] = offset

        data = self._get_data_from_response(url)
        return [Trade.from_data(trade) for trade in data]

    def place_order(
        self,
        option: int,
        price: float,
        quantity: float,
        side: OrderSide,
        order_type: Optional[str] = OrderType.LIMIT,
    ) -> Order:
        """
        Create a new option order.

        :param option: The ID of the option.
        :param price: The price of the order. Leave as None for market orders
        :param quantity: The quantity of the order.
        :param side: The side of the order (Buy or Sell).
        :param order_type: The order type (Limit or Market).
        :return: An Order instance containing the created order data.
        """
        return self.place_bulk_orders(
            [
                PlaceOrderArgs(
                    option=option,
                    price=price,
                    quantity=quantity,
                    side=side,
                    order_type=order_type,
                )
            ]
        )[0]

    def place_bulk_orders(self, orders: List[PlaceOrderArgs]) -> List[Order]:
        """
        Create new option orders.

        :param orders: A list of orders to create.
        :return: A list of Order instances containing the created order data.
        """
        url = f"{self.base_url}/options/orders/post"
        data = [
            {
                "option": order.option,
                "price": order.price,
                "quantity": order.quantity,
                "side": order.side,
                "order_type": order.order_type,
            }
            for order in orders
        ]

        data = self._post_data_and_get_response(url, data)
        return [Order.from_data(order) for order in data]

    def cancel_order(self, order_id: int) -> "Order":
        """
        Cancel an option order.

        :param order_id: The ID of the order to cancel.
        :return: An Order instance containing the canceled order data.
        """
        url = f"{self.base_url}/options/orders/cancel/{order_id}"

        data = self._post_data_and_get_response(url)
        return Order.from_data(data)

    def cancel_bulk_orders(self, order_ids: List[int]) -> List["Order"]:
        """
        Cancel multiple option orders.

        :param order_ids: A list of IDs of the orders to cancel.
        :return: A list of Order instances containing the canceled order data.
        """
        cancelled_orders = []
        for order_id in order_ids:
            try:
                cancelled_orders.append(self.cancel_order(order_id))
            except Exception as e:
                print(f"Failed to cancel order {order_id}: {e}")
        return cancelled_orders
