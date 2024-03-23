from beobachter import Logger, Stats, Plotter
from lauf import GierigLauf
from modell import Parameter

beobachter = [Logger(), Stats(), Plotter()]
#param = Parameter(min_abstand=50,sicher_abstand_ab=100)
param = Parameter()
#GierigLauf('griechenland', beobachter, param, 9).tue()
for i in range(1, 6):
	GierigLauf(f'siedler{i}', beobachter, param).tue()
