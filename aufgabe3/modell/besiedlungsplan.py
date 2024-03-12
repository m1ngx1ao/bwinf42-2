from __future__ import annotations
import math
import itertools as it
import functools as ft

from .gebiet import Gebiet
from .parameter import Parameter
from .types import TPunkt

@ft.total_ordering
class Besiedlungsplan:
	"""
	Plaene sind vergleichbar anhand ihres Losses
	"""

	LOSS_AUSSERHALB_GEBIET = 50

	def __init__(self, gebiet: Gebiet, orte: set[TPunkt],
			zentren: set[TPunkt], param: Parameter):
		self.param = param
		self.__gebiet = gebiet
		self.__orte = frozenset(orte)
		self.__zentren = frozenset(zentren)
		self.__geschuetzte_orte = frozenset(self.__berechne_geschuetzte_orte(zentren, orte))
		self.__ausserhalb_gebiet_orte = frozenset(self.__berechne_ausserhalb_gebiet_orte(orte))
		self.__loss = 0
		self.__auswerte_ort_abstand()
		self.__auswerte_gebiet()

	def __berechne_ausserhalb_gebiet_orte(self, orte: set[TPunkt]) -> set[TPunkt]:
		return {
			o for o in orte
			if not self.__gebiet.ist_drin(o)
		}

	def __berechne_geschuetzte_orte(self, zentren: set[TPunkt], orte: set[TPunkt]) -> set[TPunkt]:
		return {
			o for o in orte
			if any(
				self.__berechne_abstand(z, o) <= self.param.schutz_zentrum_bis
				for z in zentren
			)
		}

	def __auswerte_ort_abstand(self):
		zunahe_orte = set()
		for o1, o2 in list(it.combinations(self.__orte, 2)):
			erlaubter_abstand = self.param.min_abstand \
				if {o1, o2} & self.__geschuetzte_orte \
				else self.param.sicher_abstand_ab
			abstand = self.__berechne_abstand(o1, o2)
			if erlaubter_abstand > abstand:
				self.__loss += erlaubter_abstand - abstand
				zunahe_orte.update([o1, o2])
		self.__zunahe_orte = frozenset(zunahe_orte)

	def __auswerte_gebiet(self):
		self.__loss += len(self.__ausserhalb_gebiet_orte) * Besiedlungsplan.LOSS_AUSSERHALB_GEBIET

	def __berechne_abstand(self, a: TPunkt, b: TPunkt) -> float:
		ax, ay = a
		bx, by = b
		return math.sqrt(pow(bx - ax, 2) + pow(by - ay, 2))

	# OVERRIDES

	def __lt__(self, other: Besiedlungsplan) -> bool:
		return self.__loss < other.hole_loss()

	# GETTER

	def hole_loss(self) -> float:
		return self.__loss

	def hole_gebiet(self) -> Gebiet:
		return self.__gebiet

	def hole_orte(self) -> frozenset[TPunkt]:
		return self.__orte

	def hole_zentren(self) -> frozenset[TPunkt]:
		return self.__zentren

	def hole_geschuetzte_orte(self) -> frozenset[TPunkt]:
		return self.__geschuetzte_orte

	def hole_zunahe_orte(self) -> frozenset[TPunkt]:
		return self.__zunahe_orte

	def hole_ausserhalb_gebiet_orte(self) -> frozenset[TPunkt]:
		return self.__ausserhalb_gebiet_orte
