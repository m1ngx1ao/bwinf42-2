from random import random

from modell import Besiedlungsplan, TPunkt
from beobachter import Beobachter

class GierigOptimierer:
	MAX_RANDOM_BEWEGUNG = 5

	def __init__(self, plan: Besiedlungsplan, beobachter: list[Beobachter],
			budget_max_iter: int, zahl_kandidaten_pro_typ: int = 10):
		"""
		zahl_kandidaten_pro_typ bezieht sich auf den Typ der Kandidaten, naemlich:
		* Alle Punkte (Orte, Zentren) werden bewegt.
		* Nur ungueltige Punkt (Orte, die zu nah aneinander liegen) werden bewegt.
		"""
		self.__plan = plan
		self.__beobachter = beobachter
		self.__budget_max_iter = budget_max_iter
		self.__zahl_kandidaten_pro_typ = zahl_kandidaten_pro_typ

	def tue(self):
		iter_todo = self.__budget_max_iter
		plan = self.__plan
		while iter_todo > 0 and plan.hole_loss() > 0:
			kandidaten = {
					plan
				} | {
					self.__kandidat_bewege_alles(plan)
					for _ in range(self.__zahl_kandidaten_pro_typ)
				} | {
					self.__kandidat_bewege_nur_ungueltiges(plan)
					for _ in range(self.__zahl_kandidaten_pro_typ)
				}
			plan = min(kandidaten)
			for b in self.__beobachter:
				b.melde(plan)
			iter_todo -= 1
		for b in self.__beobachter:
			b.finalisiere()

	def __kandidat_bewege_alles(self, plan: Besiedlungsplan) -> Besiedlungsplan:
		orte = {
			self.__bestimme_nachfolgepunkt(o, plan)
			for o in plan.hole_orte()
		}
		zentren = {
			self.__bestimme_nachfolgepunkt(z, plan)
			for z in plan.hole_zentren()
		}
		return Besiedlungsplan(plan.hole_gebiet(), orte, zentren, plan.param, alles_im_gebiet=True)
	
	def __kandidat_bewege_nur_ungueltiges(self, plan: Besiedlungsplan) -> Besiedlungsplan:
		orte = {
			self.__bestimme_nachfolgepunkt(o, plan) if o in plan.hole_zunahe_orte() else o
			for o in plan.hole_orte()
		}
		return Besiedlungsplan(plan.hole_gebiet(), orte, plan.hole_zentren(),
			plan.param, alles_im_gebiet=True)
	
	def __bestimme_nachfolgepunkt(self, p: TPunkt, plan: Besiedlungsplan) -> TPunkt:
		while True:
			x, y = p
			x += self.MAX_RANDOM_BEWEGUNG * (random() * 2 - 1)
			y += self.MAX_RANDOM_BEWEGUNG * (random() * 2 - 1)
			if plan.hole_gebiet().ist_drin((x, y)):
				return x, y
