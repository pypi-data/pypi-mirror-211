# tests/test_sdk.py
import unittest

# from d2y.models import CreateOrder, OrderType, Side
from d2y.sdk import TradingClient
import os
from dotenv import load_dotenv
from d2y.sdk import TradingClient
from d2y.formulas import *
from d2y.enums import *
from d2y.models.order import PlaceOrderArgs

load_dotenv()

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
BASE_URL = os.environ.get("API_BASE_URL", "https://api.dev.d2y.exchange")

TEST_OPTION_ID = os.environ.get("TEST_OPTION_ID", 31617)
TEST_OPTION_STRIKE_PRICE = float(os.environ.get("TEST_OPTION_STRIKE_PRICE", 2700))
TEST_OPTION_EXPIRATION_TIMESTAMP = os.environ.get(
    "TEST_OPTION_EXPIRATION_TIMESTAMP", "2023-06-30T08:00:00Z"
)


class TestTradingClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sdk = TradingClient(API_KEY, API_SECRET, BASE_URL)

    def test_get_user(self):
        print("\n****** GETTING USER INFO ******\n")
        user = self.sdk.get_user_info()
        print("User:", user)
        for key, value in user.__dict__.items():
            print(f"{key}: {value}")

    def test_get_assets(self):
        print("\n****** GETTING ASSETS ******\n")
        assets = self.sdk.get_assets()
        for asset in assets:
            print("Asset:", asset)
            for key, value in asset.__dict__.items():
                print(f"{key}: {value}")

    def test_get_options(self):
        print("\n****** GETTING OPTIONS ******\n")
        options = self.sdk.get_options(
            expiration_timestamp=[TEST_OPTION_EXPIRATION_TIMESTAMP],
            option_type=OptionType.CALL,
            ordering="strike_price",
            strike_price=[TEST_OPTION_STRIKE_PRICE],
        )
        for option in options:
            print("Option:", option)
            for key, value in option.__dict__.items():
                print(f"{key}: {value}")

    def test_get_orderbook(self):
        print("\n****** GETTING ORDERBOOK ******\n")
        option_id = TEST_OPTION_ID
        orderbook = self.sdk.get_orderbook(option_id)
        print("Orderbook for option_id:", orderbook)

    def test_get_orders_with_pagination(self):
        print("\n****** GETTING ORDERS ******\n")
        orders = self.sdk.get_orders(status=[OrderStatus.OPEN], limit=3, offset=0)
        for order in orders[:3]:
            print("Order:", order)
            for key, value in order.__dict__.items():
                print(f"{key}: {value}")

    def test_positions(self):
        print("\n****** GETTING POSITIONS ******\n")
        positions = self.sdk.get_positions()
        for position in positions:
            print("Position:", position)
            for key, value in position.__dict__.items():
                print(f"{key}: {value}")

    def test_place_and_cancel_order(self):
        print("\n****** PLACING ORDER ******\n")
        order = self.sdk.place_order(
            option=TEST_OPTION_ID,
            price=0.01,
            quantity=2,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
        )
        print("Order:", order)
        for key, value in order.__dict__.items():
            print(f"{key}: {value}")

        print("\n****** CANCELLING ORDER ******\n")
        cancelled_order = self.sdk.cancel_order(order.id)
        print("Cancelled order:", cancelled_order)
        for key, value in cancelled_order.__dict__.items():
            print(f"{key}: {value}")

    def test_place_bulk_orders_and_get_trades(self):
        print("\n****** PLACING BULK ORDERS ******\n")
        orders = self.sdk.place_bulk_orders(
            [
                PlaceOrderArgs(
                    option=TEST_OPTION_ID,
                    price=0.01,
                    quantity=1,
                    side=OrderSide.BUY,
                    order_type=OrderType.LIMIT,
                ),
                PlaceOrderArgs(
                    option=TEST_OPTION_ID,
                    quantity=1,
                    side=OrderSide.SELL,
                    order_type=OrderType.MARKET,
                ),
            ]
        )
        for order in orders:
            print("Order:", order)
            for key, value in order.__dict__.items():
                print(f"{key}: {value}")

        print("\n****** GETTING TRADES ******\n")
        trades = self.sdk.get_trades()
        for trade in trades:
            print("Trade:", trade)
            for key, value in trade.__dict__.items():
                print(f"{key}: {value}")

    def test_calculate_option_price(self):
        print("\n****** TESTING CALCULATE_OPTION_PRICE ******\n")

        # Define parameters for the function
        S = 100.0  # Current stock price
        K = 100.0  # Strike price of the option
        T = datetime(2024, 1, 1).replace(tzinfo=pytz.UTC)  # Expiration date
        r = 0.05  # Annual risk-free interest rate, expressed as a decimal
        sigma = 0.2  # Annual volatility of the stock price, expressed as a decimal
        option_type = OptionType.CALL  # Option type (CALL or PUT)

        # Call the function with the parameters
        option_price = calculate_option_price(S, K, T, r, sigma, option_type)

        # Print the calculated option price
        print(f"Calculated option price: {option_price}")


if __name__ == "__main__":
    unittest.main()
