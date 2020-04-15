from collections import namedtuple

from misc_code.Python.investments.definitions import Bent, Cap

Strategy = namedtuple('strategy', ['Intl_Bonds', 'Intl_Stocks', 'USA_Bonds', 'USA_Stocks'])
AGGRESSIVE_STRATEGY = Strategy(
    Intl_Bonds=5.0,
    Intl_Stocks=27.5,
    USA_Bonds=15.0,
    USA_Stocks=52.5
)

CONSERVATIVE_STRATEGY = Strategy(
    Intl_Bonds=17.5,
    Intl_Stocks=12.5,
    USA_Bonds=42.5,
    USA_Stocks=27.5
)

Regions = namedtuple('regions', 'Africa, Asia_Developed, Asia_Emerging, Australasia, Canada, Europe_Emerging, Europe_Ex_Euro, Eurozone, '
                                'Japan, Latin_America, Middle_East, United_Kingdom, United_States')


REGIONAL_BALANCE = Regions(
    Africa=0.0,
    Asia_Developed=0.0,
    Asia_Emerging=0.0,
    Australasia=0.0,
    Canada=0.0,
    Europe_Emerging=0.0,
    Europe_Ex_Euro=0.0,
    Eurozone=0.0,
    Japan=0.0,
    Latin_America=0.0,
    Middle_East=0.0,
    United_Kingdom=0.0,
    United_States=0.0
)

Sectors = namedtuple('sectors', 'Basic_Materials, Communications, Consumer_Cyclical, Consumer_Defensive, Energy, Financials, Healthcare, '
                                'Industrials, Real_Estate, Technology, Utilities')
EQUAL_SECTORS = round(100.0/11.0, 2)
SECTOR_BALANCE = Sectors(
    Basic_Materials=EQUAL_SECTORS,
    Communications=EQUAL_SECTORS,
    Consumer_Cyclical=EQUAL_SECTORS,
    Consumer_Defensive=EQUAL_SECTORS,
    Energy=EQUAL_SECTORS,
    Financials=EQUAL_SECTORS,
    Healthcare=EQUAL_SECTORS,
    Industrials=EQUAL_SECTORS,
    Real_Estate=EQUAL_SECTORS,
    Technology=EQUAL_SECTORS,
    Utilities=EQUAL_SECTORS
)

BENT_BALANCE = [100/3, 100/3, 100/3]  # Growth, Blend, Value
CAP_BALANCE = [60, 20, 20]  # Large, Medium, Small


def summarize():
    caps = [f"{Cap(i + 1).name}: {per}" for i, per in enumerate(CAP_BALANCE)]
    bent = [f"{Bent(i + 1).name}: {per}" for i, per in enumerate(BENT_BALANCE)]
    
    summary = f"\nGOALS:\nCONSERVATIVE - {CONSERVATIVE_STRATEGY}\nAGGRESSIVE - {AGGRESSIVE_STRATEGY}\n\n" \
              f"Cap: {caps}\nBent: {bent}\n\n" \
              f"{SECTOR_BALANCE}\n{REGIONAL_BALANCE}"
    return summary
