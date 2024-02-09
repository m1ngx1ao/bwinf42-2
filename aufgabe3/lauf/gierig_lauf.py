from modell import Besiedlungsplan
from modell import Parameter
from ausgabe import Plotter, Waiter
from optimierung import GierigOptimierer

class GierigLauf:
	def tue(self):
		b = Besiedlungsplan(
			{
				(0, 0),
				(0, 1),
				(0, 2),
				(0, 3),
				(0, 4),
				(0, 10),
				(0, 50),
				(100, 5),
				(184, 184),
				(190, 192),
				(150, 50),
				(120, 80),
				(120, 70),
				(115, 95),
				(115, 105),
				(200, 105),
				(200, 96),
			},
			{(200, 100)},
			Parameter()
		)
		GierigOptimierer(b, [Plotter(), Waiter(.3)], 10).tue()
