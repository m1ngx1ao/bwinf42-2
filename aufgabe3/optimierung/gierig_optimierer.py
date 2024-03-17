from random import random

from modell import Besiedlungsplan, TPunkt
from beobachter import Beobachter

class GierigOptimierer:
	STRATEGIE = 'gierig'
	SYSTEM = 'optimierer'
	MAX_RANDOM_BEWEGUNG = 10
	BUDGET_MAX_ITER = 1
	ZAHL_KANDIDAT_PLAENE_BEWEGE_ALLE = 30
	ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG_UND_ZENTREN = 20
	ZAHL_KANDIDAT_PLAENE_BEWEGE_UNGUELTIG = 10

	def __init__(self, plan: Besiedlungsplan, beobachter: list[Beobachter]):
		"""
		zahl_kandidaten_pro_typ bezieht sich auf den Typ der Kandidaten, naemlich:
		* Alle Punkte (Orte, Zentren) werden bewegt.
		* Nur ungueltige Punkt (Orte, die zu nah aneinander liegen) werden bewegt.
		"""
		self.__plan = plan
		self.__beobachter = beobachter

	def tue(self) -> tuple[int, Besiedlungsplan]:
		iter_todo = self.BUDGET_MAX_ITER
		plan = self.__plan
		for b in self.__beobachter:
			b.optimierer_start(plan, self.STRATEGIE, self.SYSTEM)
		while iter_todo > 0 and plan.hole_loss() > 0:
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
			plan = min(kandidaten)
			for b in self.__beobachter:
				b.optimierer_iteration(plan)
			iter_todo -= 1
		for b in self.__beobachter:
			b.optimierer_ende()
		return (self.BUDGET_MAX_ITER - iter_todo, plan)

	def __bewege_kandidat(self, plan: Besiedlungsplan, mit_zentren: bool = False,
			mit_gueltigen: bool = False) -> Besiedlungsplan:
		orte = {
			self.__bewege_punkt(o, plan) if mit_gueltigen or o in plan.hole_zunahe_orte() else o
			for o in plan.hole_orte()
		}
		zentren = {
			self.__bewege_punkt(z, plan) if mit_zentren else z
			for z in plan.hole_zentren()
		}
		return Besiedlungsplan(plan.hole_gebiet(), orte, zentren, plan.param, alles_im_gebiet=True)
	
	def __bewege_punkt(self, p: TPunkt, plan: Besiedlungsplan) -> TPunkt:
		while True:
			x, y = p
			x += self.MAX_RANDOM_BEWEGUNG * (random() * 2 - 1)
			y += self.MAX_RANDOM_BEWEGUNG * (random() * 2 - 1)
			if plan.hole_gebiet().ist_drin((x, y)):
				return x, y
