from misc_code.Python.investments import goals
from misc_code.Python.investments.portfolio import Portfolio
from misc_code.Python.investments.symbol import Symbol


BOND_SECTORS = [0]*goals.SECTOR_BALANCE.__len__()
US_LISTING = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]

# Bonds
ILTB = Symbol('ILTB', 'Bond', 'Bond', 100, sectors=BOND_SECTORS, regions=US_LISTING)
PCY = Symbol('PCY', 'Bond', 'Bond', 100, sectors=BOND_SECTORS, regions=[5, 5, 30, 0, 0, 15, 5, 0, 0, 20, 20, 0, 0])
PTRQX = Symbol('PTRQX', 'Bond', 'Bond', 100, sectors=BOND_SECTORS, regions=[0, 10, 0, 5, 0, 0, 0, 10, 10, 0, 0, 5, 60])
SCHP = Symbol('SCHP', 'Bond', 'Bond', 100, sectors=BOND_SECTORS, regions=US_LISTING)
TAIL = Symbol('TAIL', 'Large', 'Blend', 88.2, sectors=[2.09, 10.74, 9.6, 8.14, 2.65, 13.79, 15.54, 8.71, 3.01, 22.18, 3.57],
              regions=[0, 0, 0.1, 0, 0, 0, 0.3, 0.4, 0, 0, 0, 0.6, 98.5])
VBTIX = Symbol('VBTIX', 'Bond', 'Bond', 100, sectors=BOND_SECTORS, regions=US_LISTING)

# Int'l
SCHC = Symbol('SCHC', 'Small', 'Blend', 0, sectors=[10.49, 4.02, 11.75, 5.78, 3.06, 10.6, 7.63, 20.76, 10.91, 10.84, 4.16],
              regions=[0.2, 7.4, 0.5, 6.3, 17.8, 0.6, 14.3, 18.2, 20.8, 0.1, 1.0, 12.2, 0.5])
SCHE = Symbol('SCHE', 'Large', 'Blend', 0, sectors=[0, 14.87, 14.52, 6.38, 7.13, 23.1, 3.65, 5.32, 3.44, 11.67, 2.92],
              regions=[4.4, 14.8, 59.8, 0, 0, 4.9, 0, 0.2, 0, 9.5, 5.7, 0, 0.7])
SCHF = Symbol('SCHF', 'Large', 'Blend', 0, sectors=[7.19, 6.15, 9.28, 11.52, 4.92, 17.6, 13.15, 13.85, 2.99, 9.65, 3.69],
              regions=[0, 8.3, 0.4, 5.8, 7.6, 0.3, 13.9, 25.7, 23.9, 0, 0.5, 13.0, 0.7])
VEMAX = Symbol('VEMAX', 'Large', 'Blend', 0, sectors=[7.68, 12.11, 13.49, 6.45, 7.58, 23.5, 3.69, 6.47, 3.97, 11.89, 3.18],
               regions=[5, 5, 30, 0, 0, 15, 5, 0, 0, 20, 20, 0, 0])
VT = Symbol('VT', 'Large', 'Blend', 0, sectors=[4.52, 8.59, 10.41, 7.87, 4.71, 17.43, 11.67, 11.29, 4.15, 15.94, 3.42],
            regions=[0.6, 4.2, 5.9, 2.1, 3.0, 0.8, 4.6, 8.9, 7.4, 1.4, 0.7, 5.0, 55.4])

# MISC
# real-estate
SCHH = Symbol('SCHH', 'Medium', 'Value', 0, sectors=[0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0], regions=US_LISTING)
VNQI = Symbol('VNQI', 'Medium', 'Blend', 0, sectors=[0.01, 0, 0.29, 0, 0, 0.29, 0, 0.16, 99.25, 0, 0],
              regions=[1.4, 16.0, 14.8, 8.9, 2.6, 0.5, 5.1, 14.4, 24.4, 2.1, 2.5, 7.1, 0.3])
# defense industrial
XAR = Symbol('XAR', 'Medium', 'Blend', 0, sectors=[0, 0, 0, 0, 0, 0, 0, 90.99, 0, 9.01, 0], regions=US_LISTING)

# target retirement
VTTWX = Symbol('VTTWX', 'Large', 'Blend', 32, sectors=[4.46, 8.57, 10.33, 7.66, 4.98, 17.41, 12.21, 11.37, 4.18, 15.59, 3.24],
               regions=[0, 9, 0, 5, 0, 0, 0, 9, 9, 0, 0, 5, 63])
VIRSX = Symbol('VIRSX', 'Large', 'Blend', 17.2, sectors=[4.47, 8.57, 10.33, 7.67, 4.98, 17.42, 12.21, 11.37, 4.18, 15.57, 3.24],
               regions=[0, 9, 0, 5, 0, 0, 0, 9, 9, 0, 0, 4, 62])
VTRLX = Symbol('VTRLX', 'Large', 'Blend', 10, sectors=[4.47, 8.57, 10.33, 7.67, 4.98, 17.42, 12.21, 11.37, 4.18, 15.57, 3.24],
               regions=[0, 9, 0, 5, 0, 0, 0, 9, 9, 0, 0, 4, 62])

# ETFs
POGRX = Symbol('POGRX', 'Large', 'Growth', 0, sectors=[0.34, 3.1, 10.15, 0.09, 2.2, 9.63, 30.4, 16.06, 0, 28.04, 0],
               regions=[2, 10, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 83])
SCHA = Symbol('SCHA', 'Small', 'Blend', 0, sectors=[3.51, 3.8, 9.4, 4.61, 1.72, 16.17, 16.49, 15.91, 8.83, 15.91, 3.66],
              regions=[0, 0.1, 0.1, 0, 0, 0, 0.1, 0, 0, 0.4, 0, 0.2, 99.2])
SCHB = Symbol('SCHB', 'Large', 'Blend', 0, sectors=[2.29, 9.85, 9.89, 7.48, 2.72, 13.87, 15.55, 9.1, 4.1, 21.71, 3.42],
              regions=[0, 0.1, 0.1, 0, 0, 0, 0.3, 0.4, 0, 0, 0, 0.6, 98.6])
SCHD = Symbol('SCHD', 'Large', 'Value', 0, sectors=[0.65, 4.75, 8.54, 23.1, 6.56, 7.94, 12.54, 17.77, 0.01, 18.13, 0.01],
              regions=[0, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0, 0, 99.6])
SCHG = Symbol('SCHG', 'Large', 'Growth', 0, sectors=[2.06, 13.9, 13.76, 2.71, 0.38, 11.42, 13.67, 6.29, 3.88, 30.99, 0.92],
              regions=[0, 0, 0, 0, 0, 0, 0, 0.3, 0, 0, 0, 0.9, 98.7])
SCHK = Symbol('SCHK', 'Large', 'Blend', 0, sectors=[2.18, 10.15, 9.92, 7.59, 2.74, 13.67, 15.46, 8.81, 3.87, 22.15, 3.47],
              regions=[0, 0, 0.1, 0, 0, 0, 0.3, 0.4, 0, 0, 0, 0.6, 98.5])
SCHV = Symbol('SCHV', 'Large', 'Value', 0, sectors=[2.34, 6.21, 5.47, 13.56, 5.64, 16.33, 17.58, 11.17, 3.51, 11.89, 6.3],
              regions=[0, 0.1, 0.1, 0, 0, 0, 0.6, 0.5, 0, 0, 0, 0.3, 98.3])
SCHX = Symbol('SCHX', 'Large', 'Blend', 0, sectors=[2.19, 10.36, 9.94, 7.71, 2.81, 13.68, 15.47, 8.54, 3.71, 22.19, 3.4],
              regions=[0, 0, 0.1, 0, 0, 0, 0.3, 0.4, 0, 0, 0, 0.6, 98.5])
VBK = Symbol('VBK', 'Small', 'Growth', 0, sectors=[2.17, 4.79, 10.49, 2.67, 2.14, 4.59, 21.92, 11.9, 9.95, 28.68, 0.7],
             regions=[0, 0.1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99.4])
VFTAX = Symbol('VFTAX', 'Large', 'Growth', 0, sectors=[2.14, 9.28, 8.04, 5.43, 2.35, 18.64, 16.52, 6.02, 3.99, 26.46, 1.11],
               regions=US_LISTING)
VSCIX = Symbol('VSCIX', 'Small', 'Blend', 0, sectors=[3.89, 3.11, 11.56, 3.46, 2.29, 13.94, 12.57, 15.86, 11.98, 18.17, 3.15],
               regions=US_LISTING)
VTMNX = Symbol('VTMNX', 'Large', 'Blend', 0, sectors=[7.45, 5.65, 9.99, 9.98, 5.66, 18.31, 10.85, 15.48, 3.98, 9.07, 3.6],
               regions=[5, 35, 0, 20, 0, 0, 5, 25, 10, 0, 0, 0, 0])


# example
p = Portfolio()
p.add_to_portfolio(SCHA, 25)
p.add_to_portfolio(SCHV, 25)
p.add_to_portfolio(VT, 25)
p.add_to_portfolio(PCY, 25)

print(p.summarize)
# print(goals.summarize())


""" Fidelity 401ks
SymbolSorted in ascending order. Click to reverse.	Description	Quantity	Most Recent	Change Since Close	Action
Price	Change	Value*	Dollar	Percent
FBIFX
FID FDM IDX 2040 INV
250.256	$15.88	$0.35	$3,974.06	$87.58	2.25%	Select Action for [FID FDM IDX 2040 INV]. Menu closed
FDKLX
FID FDM IDX 2060 INV
347.227	$11.45	$0.25	$3,975.74	$86.80	2.23%	Select Action for [FID FDM IDX 2060 INV]. Menu closed
FIHFX
FID FDM IDX 2035 INV
46.403	$16.26	$0.33	$754.51	$15.31	2.07%	Select Action for [FID FDM IDX 2035 INV]. Menu closed
FIKFX
FID FDM IDX INC INV
357.171	$11.85	$0.06	$4,232.47	$21.43	0.51%	Select Action for [FID FDM IDX INC INV]. Menu closed
FIPDX
FID INFL PR BD IDX
410.093	$10.56	$0.03	$4,330.58	$12.30	0.28%	Select Action for [FID INFL PR BD IDX]. Menu closed
FIPFX
FID FDM IDX 2050 INV
241.052	$16.50	$0.37	$3,977.35	$89.18	2.29%	Select Action for [FID FDM IDX 2050 INV]. Menu closed
FPIFX
FID FDM IDX 2020 INV
295.810	$14.05	$0.19	$4,156.13	$56.20	1.37%	Select Action for [FID FDM IDX 2020 INV]. Menu closed
FSGGX
FID GLB EX US IDX
273.178	$10.84	$0.20	$2,961.24	$54.63	1.88%	Select Action for [FID GLB EX US IDX]. Menu closed
FSMDX
FID MID CAP IDX
151.651	$19.02	$0.48	$2,884.40	$72.79	2.59%	Select Action for [FID MID CAP IDX]. Menu closed
FSSNX
FID SM CAP IDX
174.268	$15.67	$0.32	$2,730.77	$55.76	2.08%	Select Action for [FID SM CAP IDX]. Menu closed
FXAIX
FID 500 INDEX
32.393	$98.70	$2.94	$3,197.18	$95.23	3.07%	Select Action for [FID 500 INDEX]. Menu closed
FXIFX
FID FDM IDX 2030 INV
261.201	$15.61	$0.27	$4,077.34	$70.52	1.76%	Select Action for [FID FDM IDX 2030 INV]. Menu closed
FXNAX
FID US BOND IDX
522.716	$12.40	$0.02	$6,481.67	$10.45	0.16%	Select Action for [FID US BOND IDX]. Menu closed
GABXX.Q
GABELLI UST MM AAA
404.460	$1.00	$0.00	$404.46	$0.00	0.00%	Select Action for [GABELLI UST MM AAA]. Menu closed
Total:	$48,137.90	$728.18	1.54%

DISNEY SIP
SymbolSorted in ascending order. Click to reverse.	Description	Quantity	Most Recent	Change Since Close	Action
Price	Change	Value*	Dollar	Percent
92203Y206
VANG INST TOTL BD TR
412.951	113.660	$0.21	$46,936.01	$86.71	0.18%	Select Action for [VANG INST TOTL BD TR]. Menu closed
92206U201
VANG INST TOTL SK TR
46.127	$117.440	$3.41	$5,417.15	$157.29	2.99%	Select Action for [VANG INST TOTL SK TR]. Menu closed
FSPSX
FID INTL INDEX
73.168	$34.86	$0.65	$2,550.63	$47.55	1.90%	Select Action for [FID INTL INDEX]. Menu closed
TF25
BR EMERG MKT IDX F
350.007	$7.440	$0.12	$2,604.05	$42.00	1.63%	Select Action for [BR EMERG MKT IDX F]. Menu closed
TFMJ
BTC LIFEPATH 2025 F
1,546.418	10.710	$0.15	$16,562.13	$231.96	1.42%	Select Action for [BTC LIFEPATH 2025 F]. Menu closed
TFMO
BTC LIFEPATH 2040 F
1,434.844	11.130	$0.25	$15,969.81	$358.71	2.29%	Select Action for [BTC LIFEPATH 2040 F]. Menu closed
TFMT
BTC LIFEPATH 2055 F
929.187	11.280	$0.28	$10,481.22	$260.17	2.54%	Select Action for [BTC LIFEPATH 2055 F]. Menu closed
VMCPX
VANG MD CP IDX IS PL
25.543	$196.72	$5.15	$5,024.81	$131.54	2.69%	Select Action for [VANG MD CP IDX IS PL]. Menu closed
VSCPX
VANG SM CP IDX IS PL
26.858	$173.15	$3.85	$4,650.46	$103.40	2.27%	Select Action for [VANG SM CP IDX IS PL]. Menu closed
Total:	$110,196.27	$1,419.33	1.30%
"""