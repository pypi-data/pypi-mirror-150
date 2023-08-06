from enum import Enum


class Events(Enum):
    MAIN = "main"
    SECONDARY = "secondary"


class Actions(Enum):
    BUY = "BUY"
    SELL = "SELL"
