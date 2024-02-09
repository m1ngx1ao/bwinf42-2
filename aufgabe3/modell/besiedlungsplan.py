from __future__ import annotations
import math
import itertools as it
import functools as ft

from .parameter import Parameter

TPunkt = tuple[float, float]

@ft.total_ordering
class Besiedlungsplan:
	"""
	Plaene sind vergleichbar anhand ihres Losses
	"""

	def __init__(self, orte: set[TPunkt],
			zentren: set[TPunkt], param: Parameter):
		self.param = param
		self.__orte = frozenset(orte)
		self.__zentren = frozenset(zentren)
		self.__geschuetzte_orte = frozenset(self.__berechne_geschuetzte_orte(zentren, orte))
		self.__auswerte_ort_abstand()

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
		loss = 0
		for o1, o2 in list(it.combinations(self.__orte, 2)):
			erlaubter_abstand = self.param.min_abstand \
				if {o1, o2} & self.__geschuetzte_orte \
				else self.param.sicher_abstand_ab
			abstand = self.__berechne_abstand(o1, o2)
			if erlaubter_abstand > abstand:
				loss += erlaubter_abstand - abstand
				zunahe_orte.update([o1, o2])
		self.__zunahe_orte = frozenset(zunahe_orte)
		self.__loss = loss

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

	def hole_orte(self) -> frozenset[TPunkt]:
		return self.__orte

	def hole_zentren(self) -> frozenset[TPunkt]:
		return self.__zentren

	def hole_geschuetzte_orte(self) -> frozenset[TPunkt]:
		return self.__geschuetzte_orte

	def hole_zunahe_orte(self) -> frozenset[TPunkt]:
		return self.__zunahe_orte
