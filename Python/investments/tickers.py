from misc_code.Python.investments import goals
from misc_code.Python.investments.portfolio import Portfolio
from misc_code.Python.investments.symbol import Symbol

US_LISTING = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]  # entirely domestic holdings

SCHA = Symbol('SCHA', 'Small', 'Blend', 0, [3.57, 3.72, 11.19, 3.88, 2.50, 16.88, 14.41, 15.90, 10.29, 14.47, 3.18], US_LISTING)
SCHB = Symbol('SCHB', 'Large', 'Blend', 0, [2.30, 9.70, 10.23, 6.67, 3.48, 15.61, 13.81, 9.88, 4.34, 20.69, 3.29], US_LISTING)
SCHD = Symbol('SCHD', 'Large', 'Value', 0, [0.67, 4.72, 9.61, 22.81, 5.84, 9.54, 12.19, 16.61, 0.01, 17.98, 0.01], US_LISTING)
SCHG = Symbol('SCHG', 'Large', 'Growth', 0, [1.98, 14.11, 13.65, 2.53, 0.50, 12.25, 12.77, 7.62, 3.45, 30.23, 0.89], US_LISTING)
SCHK = Symbol('SCHK', 'Large', 'Blend', 0, [2.17, 10.03, 10.16, 6.82, 3.49, 15.49, 13.72, 9.55, 4.00, 21.22, 3.36], US_LISTING)
SCHV = Symbol('SCHV', 'Large', 'Value', 0, [2.40, 5.94, 6.17, 11.90, 7.03, 19.14, 14.87, 11.19, 4.13, 11.21, 6.01], US_LISTING)
SCHX = Symbol('SCHX', 'Large', 'Blend', 0, [2.18, 10.27, 10.14, 6.94, 3.57, 15.49, 13.76, 9.30, 3.77, 21.29, 3.30], US_LISTING)
VBK = Symbol('VBK', 'Small', 'Growth', 0, [2.37, 4.65, 10.75, 2.57, 2.47, 4.74, 20.86, 12.39, 10.07, 28.43, 0.70], US_LISTING)
VOOV = Symbol('VOOV', 'Large', 'Value', 0, [1.97, 7.54, 5.60, 9.81, 7.21, 21.32, 18.55, 10.24, 3.34, 7.58, 6.83], US_LISTING)
VUG = Symbol('VUG', 'Large', 'Growth', 0, [1.93, 14.30, 15.89, 3.18, 1.16, 9.88, 8.40, 7.99, 4.83, 32.42, 0.03], US_LISTING)


# example
p = Portfolio()
p.add_to_portfolio(SCHA, 50)
p.add_to_portfolio(SCHV, 50)

print(p.summarize)
print(goals.summarize())
