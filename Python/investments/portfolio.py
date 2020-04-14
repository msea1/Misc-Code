import misc_code.Python.investments.definitions
from misc_code.Python.investments import constants, exceptions, goals, symbol


class Portfolio:
    def __init__(self):
        self.budget_left = constants.BUDGET_START
        self.budget_spent = 0
        self.holdings = {}
    
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
        if self.budget_left == constants.BUDGET_START:
            return 'Nothing added yet'
        strategy = self.summarize_strategy()
        sectors = self.summarize_sectors()
        regions = self.summarize_regions()
        caps = self.summarize_cap()
        bent = self.summarize_bent()
        
        summary = f"\nBUDGET: {constants.BUDGET_START}\nREMAINING: {self.budget_left}\n" \
                  f"{strategy}\nCap: {caps}\nBent: {bent}\n\n{sectors}\n{regions}"
        return summary
    
    def summarize_strategy(self):
        percentages = [0]*misc_code.Python.investments.definitions.Group.__len__()
        for holding, percentage in self.holdings.items():
            percentages[holding.grouping.value - 1] += (percentage/self.budget_spent*100)
        return goals.Strategy(*percentages)
    
    def summarize_cap(self):
        percentages = [0]*misc_code.Python.investments.definitions.Cap.__len__()
        for holding, percentage in self.holdings.items():
            percentages[holding.cap.value - 1] += (percentage/self.budget_spent*100)
        caps = [f"{symbol.Cap(i + 1).name}: {per}" for i, per in enumerate(percentages)]
        return caps
    
    def summarize_bent(self):
        percentages = [0]*misc_code.Python.investments.definitions.Bent.__len__()
        for holding, percentage in self.holdings.items():
            percentages[holding.bent.value - 1] += (percentage/self.budget_spent*100)
        caps = [f"{symbol.Bent(i + 1).name}: {per}" for i, per in enumerate(percentages)]
        return caps
    
    def summarize_sectors(self):
        percentages = [0]*goals.SECTOR_BALANCE.__len__()
        for holding, percentage in self.holdings.items():
            for i in range(len(percentages)):
                percentages[i] += (holding.sector_weights[i]*percentage/self.budget_spent)
        return goals.Sectors(*percentages)
    
    def summarize_regions(self):
        percentages = [0]*goals.REGIONAL_BALANCE.__len__()
        for holding, percentage in self.holdings.items():
            for i in range(len(percentages)):
                percentages[i] += (holding.regional_distribution[i]*percentage/self.budget_spent)
        return goals.Regions(*percentages)


# TODO list
#   handle real estate sector
#   add more tickers
#   regional weighting goal?
#   validators
#   decision/re-weighting model?
