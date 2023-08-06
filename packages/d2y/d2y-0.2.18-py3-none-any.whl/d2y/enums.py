from enum import Enum


class OrderType(str, Enum):
    LIMIT = "Limit"
    MARKET = "Market"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def list(cls):
        return [key.value for key in cls]


class OptionType(str, Enum):
    CALL = "Call"
    PUT = "Put"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def list(cls):
        return [key.value for key in cls]


class SettlementPeriodType(str, Enum):
    DAILY = "Day"
    WEEKLY = "Week"
    MONTHLY = "Month"
    QUARTER = "Quarter"    
    OTHER = "Other"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def list(cls):
        return [key.value for key in cls]


class OrderSide(str, Enum):
    BUY = "Buy"
    SELL = "Sell"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def list(cls):
        return [key.value for key in cls]


class OrderStatus(str, Enum):
    OPEN = "Open"
    FILLED = "Filled"
    CANCELLED = "Cancelled"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def list(cls):
        return [key.value for key in cls]


class TransferType(str, Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def list(cls):
        return [key.value for key in cls]


class TransferStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def list(cls):
        return [key.value for key in cls]
