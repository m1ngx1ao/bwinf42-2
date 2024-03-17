from beobachter import Logger, Stats, Plotter
from lauf import GierigLauf

#GierigLauf('siedler3').tue()
for i in range(1, 6):
	GierigLauf(f'siedler{i}', [Logger(), Stats(), Plotter()]).tue()
