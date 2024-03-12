from modell import Besiedlungsplan, Gebiet, Parameter
from beobachter import Plotter, Logger, Stats
from optimierung import GierigOptimierer

class GierigLauf:
	def tue(self):
		b = Besiedlungsplan(
			Gebiet.von_datei('input/siedler1.txt'),
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
		lauf_name = __class__.__name__
		GierigOptimierer(b, [
			Logger(lauf_name),
			Stats(lauf_name),
			Plotter(lauf_name)
		], 10).tue()
