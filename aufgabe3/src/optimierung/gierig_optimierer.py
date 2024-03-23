from random import random

from modell import Besiedlungsplan, TPunkt
from beobachter import Beobachter

class GierigOptimierer:
	STRATEGIE = 'gierig'
	MAX_RANDOM_BEWEGUNG = 10
	"""
	Die maximale Entfernung, die ein Punkt bei der Kandidaterstellung
	verschoben werden kann - nach der Tschebyschew-Norm, also max(dx, dy)
	"""

	BUDGET_MAX_ITER = 100
	BUDGET_MAX_ITER_OHNE_FORTSCHRITT = 10

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
		iter_num_ohne_fortschritt = 0
		while iter_num_ohne_fortschritt < self.BUDGET_MAX_ITER_OHNE_FORTSCHRITT \
				and iter_num < self.BUDGET_MAX_ITER and plan.hole_loss() > 0:
			iter_num += 1
			iter_num_ohne_fortschritt += 1
			kandidaten = {
					self.__bewege_kandidat(plan, mit_zentrum=True, mit_gueltigen=True)
					for _ in range(self.ZAHL_KANDIDAT_PLAENE_BEWEGE_ALLE)
				} | {
					self.__bewege_kandidat(plan, mit_zentrum=True, mit_ungueltigen=False)
					for _ in range(self.ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG_UND_ZENTREN)
				} | {
					self.__bewege_kandidat(plan)
					for _ in range(self.ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG)
				}
			# gierige Wahl: Fahre mit Kandidaten fort, der geringsten Loss hat
			bester_kandidat = min(kandidaten)
			if bester_kandidat.hole_loss() < plan.hole_loss():
				plan = bester_kandidat
				iter_num_ohne_fortschritt = 0
			for b in self.__beobachter:
				b.optimierer_iteration(plan)
		for b in self.__beobachter:
			b.optimierer_ende()
		return iter_num, plan

	def __bewege_kandidat(self, plan: Besiedlungsplan, mit_zentrum: bool = False,
			mit_gueltigen: bool = False, mit_ungueltigen: bool = True) -> Besiedlungsplan:
		orte = {
			self.__bewege_punkt(o, plan)
			if mit_gueltigen or (mit_ungueltigen and o in plan.hole_zunahe_orte())
			else o
			for o in plan.hole_orte()
		}
		zentrum_idx = int(random() * len(plan.hole_zentren())) if mit_zentrum else -1
		zentren = {
			self.__bewege_punkt(z, plan) if idx == zentrum_idx else z
			for idx, z in enumerate(plan.hole_zentren())
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
