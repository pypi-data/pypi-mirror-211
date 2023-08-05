from enum import IntEnum, Enum

class Provider(Enum, str):
    ALPACA = "alpaca"
    ROBINHOOD = "robinhood"

class PurchaseStrategy(IntEnum):
    CHEAPEST_FIRST = 1
    LARGEST_DIFF_FIRST = 2


class RoundingStrategy(Enum, int):
    CLOSEST = 1
    FLOOR = 2
    CEILING = 3


class Currency(Enum, str):
    USD = "$"
    EURO = "€"
    POUND = "£"
