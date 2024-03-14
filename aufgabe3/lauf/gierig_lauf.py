from random import random

from modell import Besiedlungsplan, Gebiet, Parameter, TPunkt
from beobachter import Plotter, Logger, Stats
from optimierung import GierigOptimierer

class GierigLauf:
	
	def tue(self):
		gebiet = Gebiet.von_datei('input/siedler2.txt')
		b = Besiedlungsplan(
			gebiet,
			{self.__hole_ort(gebiet) for _ in range(80)},
			{self.__hole_ort(gebiet) for _ in range(1)},
			Parameter(),
			alles_im_gebiet=True
		)
		lauf_name = __class__.__name__
		GierigOptimierer(b, [
			Logger(lauf_name),
			Stats(lauf_name),
			Plotter(lauf_name)
		], 300).tue()

	def __hole_ort(self, g: Gebiet) -> TPunkt:
		xs, ys = zip(*g.hole_eckpunkte())
		min_x, max_x = min(*xs), max(*xs)
		min_y, max_y = min(*ys), max(*ys)
		while True:
			x = (max_x - min_x) * random() + min_x
			y = (max_y - min_y) * random() + min_y
			if g.ist_drin((x, y)):
				return x, y
