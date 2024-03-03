import random

from modell import Besiedlungsplan, TPunkt
from beobachter import Beobachter

class GierigOptimierer:
	MAX_RANDOM_BEWEGUNG = 5

	def __init__(self, plan: Besiedlungsplan, beobachter: list[Beobachter],
			budget_max_iter: int, zahl_kandidaten: int = 10):
		self.__plan = plan
		self.__beobachter = beobachter
		self.__budget_max_iter = budget_max_iter
		self.__zahl_kandidaten = zahl_kandidaten

	def tue(self):
		iter_todo = self.__budget_max_iter
		plan = self.__plan
		while iter_todo > 0 and plan.hole_loss() > 0:
			kandidaten = {plan} | {self.__bestimme_kandidat(plan) for _ in range(self.__zahl_kandidaten)}
			plan = min(kandidaten)
			for b in self.__beobachter:
				b.melde(plan)
			iter_todo -= 1
		for b in self.__beobachter:
			b.finalisiere()

	def __bestimme_kandidat(self, plan: Besiedlungsplan) -> Besiedlungsplan:
		orte = {
			self.__bestimme_punkt(o)
			for o in plan.hole_orte()	
		}
		zentren = {
			self.__bestimme_punkt(z)
			for z in plan.hole_zentren()
		}
		return Besiedlungsplan(orte, zentren, plan.param)
	
	def __bestimme_punkt(self, p: TPunkt) -> TPunkt:
		x, y = p
		x += self.MAX_RANDOM_BEWEGUNG * (random.random() * 2 - 1)
		y += self.MAX_RANDOM_BEWEGUNG * (random.random() * 2 - 1)
		return x, y