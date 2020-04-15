from misc_code.Python.investments import goals
from misc_code.Python.investments.portfolio import Portfolio
from misc_code.Python.investments.symbol import Symbol
'''
SCHE
SCHF
SCHH
SCHP
TAIL
VNQI
'''
BOND_SECTORS = [0]*goals.SECTOR_BALANCE.__len__()
US_LISTING = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]
# Bonds
ILTB = Symbol('ILTB', 'Bond', 'Bond', 100, sectors=BOND_SECTORS, regions=US_LISTING)
PCY = Symbol('PCY', 'Bond', 'Bond', 100, sectors=BOND_SECTORS, regions=US_LISTING)  # TODO has foreign bonds

# Int'l
SCHC = Symbol('SCHC', 'Small', 'Blend', 0, sectors=[10.49, 4.02, 11.75, 5.78, 3.06, 10.6, 7.63, 20.76, 10.91, 10.84, 4.16],
              regions=[0.2, 7.4, 0.5, 6.3, 17.8, 0.6, 14.3, 18.2, 20.8, 0.1, 1.0, 12.2, 0.5])
VT = Symbol('VT', 'Large', 'Value', 0, sectors=[4.52, 8.59, 10.41, 7.87, 4.71, 17.43, 11.67, 11.29, 4.15, 15.94, 3.42],
            regions=[0.6, 4.2, 5.9, 2.1, 3.0, 0.8, 4.6, 8.9, 7.4, 1.4, 0.7, 5.0, 55.4])

# Misc
XAR = Symbol('XAR', 'Large', 'Value', 0, sectors=[0, 0, 0, 0, 0, 0, 0, 90.99, 0, 9.01, 0], regions=US_LISTING)

# ETFs
SCHA = Symbol('SCHA', 'Small', 'Blend', 0, sectors=[3.51, 3.8, 9.4, 4.61, 1.72, 16.17, 16.49, 15.91, 8.83, 15.91, 3.66],
              regions=[0.0, 0.1, 0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.4, 0.0, 0.2, 99.2])
SCHB = Symbol('SCHB', 'Large', 'Blend', 0, sectors=[2.29, 9.85, 9.89, 7.48, 2.72, 13.87, 15.55, 9.1, 4.1, 21.71, 3.42],
              regions=[0.0, 0.1, 0.1, 0.0, 0.0, 0.0, 0.3, 0.4, 0.0, 0.0, 0.0, 0.6, 98.6])
SCHD = Symbol('SCHD', 'Large', 'Value', 0, sectors=[0.65, 4.75, 8.54, 23.1, 6.56, 7.94, 12.54, 17.77, 0.01, 18.13, 0.01],
              regions=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 99.6])
SCHG = Symbol('SCHG', 'Large', 'Growth', 0, sectors=[2.06, 13.9, 13.76, 2.71, 0.38, 11.42, 13.67, 6.29, 3.88, 30.99, 0.92],
              regions=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.9, 98.7])
SCHK = Symbol('SCHK', 'Large', 'Blend', 0, sectors=[2.18, 10.15, 9.92, 7.59, 2.74, 13.67, 15.46, 8.81, 3.87, 22.15, 3.47],
              regions=[0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.3, 0.4, 0.0, 0.0, 0.0, 0.6, 98.5])
SCHV = Symbol('SCHV', 'Large', 'Value', 0, sectors=[2.34, 6.21, 5.47, 13.56, 5.64, 16.33, 17.58, 11.17, 3.51, 11.89, 6.3],
              regions=[0.0, 0.1, 0.1, 0.0, 0.0, 0.0, 0.6, 0.5, 0.0, 0.0, 0.0, 0.3, 98.3])
SCHX = Symbol('SCHX', 'Large', 'Blend', 0, sectors=[2.19, 10.36, 9.94, 7.71, 2.81, 13.68, 15.47, 8.54, 3.71, 22.19, 3.4],
              regions=[0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.3, 0.4, 0.0, 0.0, 0.0, 0.6, 98.5])
VBK = Symbol('VBK', 'Small', 'Growth', 0, sectors=[2.17, 4.79, 10.49, 2.67, 2.14, 4.59, 21.92, 11.9, 9.95, 28.68, 0.7],
             regions=[0.0, 0.1, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 99.4])


# example
p = Portfolio()
p.add_to_portfolio(SCHA, 25)
p.add_to_portfolio(SCHV, 25)
p.add_to_portfolio(VT, 25)
p.add_to_portfolio(PCY, 25)

print(p.summarize)
# print(goals.summarize())
