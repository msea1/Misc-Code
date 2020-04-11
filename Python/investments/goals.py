from collections import namedtuple

# TODO validator that it adds to 100
Strategy = namedtuple('strategy', ['Alternatives', 'Intl_Bonds', 'Intl_Stocks', 'USA_Bonds', 'USA_Stocks'])
AGGRESSIVE_STRATEGY = Strategy(
    Alternatives=5.0,
    Intl_Bonds=5.0,
    Intl_Stocks=25.0,
    USA_Bonds=15.0,
    USA_Stocks=50.0
)

CONSERVATIVE_STRATEGY = Strategy(
    Alternatives=10.0,
    Intl_Bonds=15.0,
    Intl_Stocks=10.0,
    USA_Bonds=40.0,
    USA_Stocks=25.0
)

Regions = namedtuple('regions', 'Africa, Asia_Developed, Asia_Emerging, Australasia, Canada, Europe_Emerging, Europe_NonEU, Eurozone, '
                                'Japan, Latin_America, Middle_East, United_Kingdom, United_States')
REGIONAL_BALANCE = Regions(
    Africa=0.0,
    Asia_Developed=0.0,
    Asia_Emerging=0.0,
    Australasia=0.0,
    Canada=0.0,
    Europe_Emerging=0.0,
    Europe_NonEU=0.0,
    Eurozone=0.0,
    Japan=0.0,
    Latin_America=0.0,
    Middle_East=0.0,
    United_Kingdom=0.0,
    United_States=0.0
)

Sectors = namedtuple('sectors', 'Basic_Materials, Communications, Consumer_Cyclical, Consumer_Defensive, Energy, Financials, Healthcare, '
                                'Industrials, Real_Estate, Technology, Utilities')
SECTOR_BALANCE = Sectors(
    Basic_Materials=10.0,
    Communications=10.0,
    Consumer_Cyclical=10.0,
    Consumer_Defensive=10.0,
    Energy=10.0,
    Financials=10.0,
    Healthcare=10.0,
    Industrials=10.0,
    Real_Estate=0.0,
    Technology=10.0,
    Utilities=10.0
)

BENT_BALANCE = [100/3, 100/3, 100/3]  # Growth, Blend, Value
CAP_BALANCE = [60, 20, 20]  # Large, Medium, Small
