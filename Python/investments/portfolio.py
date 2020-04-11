from . import tickers
from .exceptions import ExceededBudgetError


class Portfolio:
    def __init__(self):
        self.budget_percentage = 100.0
        self.holdings = {}
        
    @property
    def summarize(self):
        return self.holdings
    
    def add_to_portfolio(self, ticker_symbol, percentage):
        if percentage > self.budget_percentage:
            raise ExceededBudgetError(f'failed to add {ticker_symbol} at level {percentage} to portfolio. '
                                      f'Only {self.budget_percentage} remains')
        self.budget_percentage -= percentage
        if ticker_symbol in self.holdings:
            self.holdings[ticker_symbol] += percentage
        else:
            self.holdings[ticker_symbol] = percentage


# example
p = Portfolio()
p.add_to_portfolio(tickers.SCHA, 50)
