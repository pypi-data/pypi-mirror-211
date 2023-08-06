# D2Y Python SDK

The D2Y Python SDK is a convenient and user-friendly library for interacting with the D2Y Exchange API. It simplifies the process of accessing and managing data from the D2Y platform and offers an easy-to-use interface for developers.

## Installation

To install the D2Y Python SDK, use pip:

```
pip install --index-url https://test.pypi.org/simple/ --upgrade d2y
```

## Features

- Retrieve and manage user data, including balances and profile information
- Access and manipulate asset, option, and order data
- Intuitive and easy-to-use interface for developers

## Usage

Here's an example of how to use the D2Y Python SDK:

```python
from d2y.sdk import TradingClient
from d2y.models import Side


# Initialize the D2YExchange object with your API key
client = TradingClient(API_KEY, API_SECRET) # Get API KEY and SECRET from d2y.exchange

# Get user data
user = client.get_user_data()

# List all available assets
assets = client.get_assets()

# Retrieve options data
options = client.get_options()

# Place a single order
created_order = self.sdk.place_order(option=71, price="100", quantity="1", side=Side.BUY, order_type=OrderType.LIMIT)

# Place a bulk orders
orders =
[
    CreateOrder(option=71, price=100, quantity=1, side=OrderSide.BUY, order_type=OrderType.LIMIT),
    CreateOrder(option=72, price=20, quantity=1, side=OrderSide.BUY, order_type=OrderType.LIMIT),
    CreateOrder(option=73, price=80, quantity=1, side=OrderSide.SELL, order_type=OrderType.MARKET)
]

created_orders = self.sdk.place_bulk_orders(orders)

# cancel an order
cancelled_order = self.sdk.cancel_order(created_order.id)
```

## Documentation

For complete documentation and detailed examples, please visit our [official SDK documentation](https://docs.sdk.d2y.exchange/).

## Generate Sphinx Documentation

To generate the Sphinx documentation for the SDK, follow these steps:

Ensure you have Sphinx installed. If not, install it using pip:

```
pip install sphinx
```

Navigate to the docs directory of the SDK:

```
cd path/to/d2y/python_sdk/docs
```

Run the following command to generate the documentation:

```
make html
```

The generated documentation can be found in the build/html directory.

```
open /build/html/index.html
```

## How to push to PyPi

Make sure you have the latest version of the code.

Bump the version number in the setup.py file, for example from 1.0.0 to 1.0.1.

Build the package by running the following command from the root of the project:

```
python setup.py sdist bdist_wheel
```

Upload the package to TestPyPI by running the following command:

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

You will be prompted to enter your TestPyPI username and password. If you haven't created a TestPyPI account yet, you can create one at https://test.pypi.org/account/register/.

Install the package from TestPyPI to verify that everything works as expected:

```
pip install --index-url https://test.pypi.org/simple/ --upgrade d2y
```

This should install the development version of the package that you just uploaded.

Note: make sure to only upload development versions to TestPyPI, and only stable versions to PyPI.

## Tests

`python -m unittest tests.test_sdk`

## Support

If you encounter any issues or have questions about the SDK, please feel free to reach out to our support team at support@d2y.exchange or visit our [community forum](https://community.d2y.exchange).

## License

The D2Y Python SDK is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
