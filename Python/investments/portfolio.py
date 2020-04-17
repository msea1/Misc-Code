import json

from misc_code.Python.investments import constants, exceptions, goals, symbol
from misc_code.Python.investments.constants import SIGDIF
from misc_code.Python.investments.definitions import Bent, Cap


class Portfolio:
    def __init__(self):
        self.budget_left = constants.BUDGET_START
        self.budget_spent = 0
        self.holdings = {}
        self.bond_spend = 0
    
    def add_to_portfolio(self, ticker_symbol: symbol.Symbol, percentage):
        if percentage > self.budget_left:
            raise exceptions.ExceededBudgetError(f'failed to add {ticker_symbol} at level {percentage} to portfolio. '
                                                 f'Only {self.budget_left} remains')
        self.budget_left -= percentage
        self.budget_spent += percentage
        if ticker_symbol in self.holdings:
            self.holdings[ticker_symbol] += percentage
        else:
            self.holdings[ticker_symbol] = percentage
    
    @property
    def summarize(self):
        if self.budget_spent == 0:
            return 'Nothing added yet'
        portfolio_summary = {k.ticker: v for k, v in self.holdings.items()}
        strategy = self.summarize_strategy()
        sectors = self.summarize_sectors()
        regions = self.summarize_regions()
        caps = self.summarize_cap()
        bent = self.summarize_bent()
        
        summary = f"\nBUDGET: {constants.BUDGET_START}\nREMAINING: {self.budget_left}\n" \
                  f"PORTFOLIO: {json.dumps(portfolio_summary, indent=4, sort_keys=True)}\n\n" \
                  f"STRATEGY: {json.dumps(strategy._asdict(), indent=4, sort_keys=True)}\n" \
                  f"Cap: {caps}\nBent: {bent}\n\n" \
                  f"SECTORS: {json.dumps(sectors._asdict(), indent=4, sort_keys=True)}\n" \
                  f"REGIONS: {json.dumps(regions._asdict(), indent=4, sort_keys=True)}"
        return summary
    
    def summarize_strategy(self):
        percentages = {'Intl_Bonds': 0, 'Intl_Stocks': 0, 'USA_Bonds': 0, 'USA_Stocks': 0}
        for holding, percentage in self.holdings.items():
            foreign, domestic = holding.foreign_domestic_weight
            percentages['Intl_Bonds'] += round(holding.bond_percentage*foreign/self.budget_spent*percentage/100, SIGDIF)
            percentages['Intl_Stocks'] += round((100 - holding.bond_percentage)*foreign/self.budget_spent*percentage/100, SIGDIF)
            percentages['USA_Bonds'] += round(holding.bond_percentage*domestic/self.budget_spent*percentage/100, SIGDIF)
            percentages['USA_Stocks'] += round((100 - holding.bond_percentage)*domestic/self.budget_spent*percentage/100, SIGDIF)
        self.bond_spend = percentages['Intl_Bonds'] + percentages['USA_Bonds']
        return goals.Strategy(**percentages)
    
    def summarize_cap(self):
        percentages = [0]*(Cap.__len__() - 1)
        for holding, percentage in self.holdings.items():
            if holding.bent.value > len(percentages):
                continue
            percentages[holding.cap.value - 1] += (percentage/(self.budget_spent - self.bond_spend)*100)
        caps = [f"{symbol.Cap(i + 1).name}: {round(per, SIGDIF)}" for i, per in enumerate(percentages)]
        return caps
    
    def summarize_bent(self):
        percentages = [0]*(Bent.__len__() - 1)
        for holding, percentage in self.holdings.items():
            if holding.bent.value > len(percentages):
                continue
            percentages[holding.bent.value - 1] += (percentage/(self.budget_spent - self.bond_spend)*100)
        bents = [f"{symbol.Bent(i + 1).name}: {round(per, SIGDIF)}" for i, per in enumerate(percentages)]
        return bents
    
    def summarize_sectors(self):
        percentages = [0]*goals.SECTOR_BALANCE.__len__()
        for holding, percentage in self.holdings.items():
            for i in range(len(percentages)):
                percentages[i] += round(holding.sector_weights[i]*percentage/(self.budget_spent - self.bond_spend), SIGDIF)
        return goals.Sectors(*percentages)
    
    def summarize_regions(self):
        percentages = [0]*goals.REGIONAL_BALANCE.__len__()
        for holding, percentage in self.holdings.items():
            for i in range(len(percentages)):
                percentages[i] += round(holding.regional_distribution[i]*percentage/self.budget_spent, SIGDIF)
        return goals.Regions(*percentages)

# TODO list
#   add 401k tickers, options to sector balance
#   change balancing to be additive of actual shares rather than constrain 100 budget
#   add my current portfolio
#   regional weighting goal?
#   decision/re-weighting model?
#   remove mid cap?
