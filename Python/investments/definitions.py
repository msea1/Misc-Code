from enum import Enum, auto


class Bent(Enum):
    Growth = auto()
    Blend = auto()
    Value = auto()


class Cap(Enum):
    Small = auto()
    Medium = auto()
    Large = auto()


class Group(Enum):
    Alternatives = auto()
    Intl_Bonds = auto()
    Intl_Stocks = auto()
    USA_Bonds = auto()
    USA_Stocks = auto()