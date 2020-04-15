from typing import List, Tuple

from .definitions import Bent, Cap
from .goals import Regions, Sectors


class Symbol:
    def __init__(self, ticker: str, cap: str, gbv: str, bonds: float, sectors: List[float], regions: List[float]):
        self.ticker = ticker
        self.cap = Cap[cap]
        self.bent = Bent[gbv]
        self.bond_percentage = bonds
        self.sector_weights = Sectors(*sectors)
        self.regional_distribution = Regions(*regions)
    
    def __repr__(self) -> str:
        return f'{self.ticker.upper()}'
    
    def __lt__(self, other: "Symbol") -> bool:
        return self.ticker < other.ticker
    
    @property
    def foreign_domestic_weight(self) -> Tuple[float, float]:
        total = sum(self.regional_distribution)
        domestic_weight = self.regional_distribution.United_States
        return (total - domestic_weight), domestic_weight
