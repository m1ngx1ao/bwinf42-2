from random import random

from modell import Besiedlungsplan, TPunkt
from beobachter import Beobachter

class GierigOptimierer:
	STRATEGIE = 'gierig'
	MAX_RANDOM_BEWEGUNG = 10
	BUDGET_MAX_ITER = 100

	ZAHL_KANDIDAT_PLAENE_BEWEGE_ALLE = 30
	ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG_UND_ZENTREN = 20
	ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG = 10

	def __init__(self, plan: Besiedlungsplan, beobachter: list[Beobachter]):
		self.__plan = plan
		self.__beobachter = beobachter

	def tue(self) -> tuple[int, Besiedlungsplan]:
		iter_num = 0
		plan = self.__plan
		for b in self.__beobachter:
			b.optimierer_start(plan, self.STRATEGIE)
		while iter_num < self.BUDGET_MAX_ITER and plan.hole_loss() > 0:
			iter_num += 1
			kandidaten = {
					plan
				} | {
					self.__bewege_kandidat(plan, mit_zentren=True, mit_gueltigen=True)
					for _ in range(self.ZAHL_KANDIDAT_PLAENE_BEWEGE_ALLE)
				} | {
					self.__bewege_kandidat(plan, mit_zentren=True)
					for _ in range(self.ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG_UND_ZENTREN)
				} | {
					self.__bewege_kandidat(plan)
					for _ in range(self.ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG)
				}
			# gierige Wahl: Fahre mit Kandidaten fort, der geringsten Loss hat
			plan = min(kandidaten)
			for b in self.__beobachter:
				b.optimierer_iteration(plan)
		for b in self.__beobachter:
			b.optimierer_ende()
		return iter_num, plan

	def __bewege_kandidat(self, plan: Besiedlungsplan, mit_zentren: bool = False,
			mit_gueltigen: bool = False) -> Besiedlungsplan:
		orte = {
			self.__bewege_punkt(o, plan)
			if mit_gueltigen or o in plan.hole_zunahe_orte()
			else o
			for o in plan.hole_orte()
		}
		zentren = {
			self.__bewege_punkt(z, plan) if mit_zentren else z
			for z in plan.hole_zentren()
		}
		return Besiedlungsplan(
			plan.hole_gebiet(),
			orte,
			zentren,
			plan.param,
			alles_im_gebiet=True
		)
	
	def __bewege_punkt(self, p: TPunkt, plan: Besiedlungsplan) -> TPunkt:
		while True:
			x, y = p
			x += self.MAX_RANDOM_BEWEGUNG * (random() * 2 - 1)
			y += self.MAX_RANDOM_BEWEGUNG * (random() * 2 - 1)
			if plan.hole_gebiet().ist_drin((x, y)):
				return x, y
