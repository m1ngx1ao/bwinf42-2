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
	"""
	Fester Loss fuer Ortschaft ausserhalb des Gebiets
	unabhaengig vom Abstand zu Gebietsgrenzen
	Wird in Optimierung nicht verwendet, da nur Punkte innerhalb des Gebiets
	gesetzt und verschoben werden.
	"""

	def __init__(self, gebiet: Gebiet, orte: set[TPunkt] | frozenset[TPunkt],
			zentren: set[TPunkt] | frozenset[TPunkt], param: Parameter,
			alles_im_gebiet: bool = False):
		"""
		alles_im_gebiet bedeuet, dass der Aufrufer schon von sich aus sichergestellt hat,
		dass alle Orte und Zentren innerhalb des Gebiets liegen.
		"""
		self.param = param
		self.__gebiet = gebiet
		self.__orte = frozenset(orte)
		self.__zentren = frozenset(zentren)
		self.__geschuetzte_orte = frozenset(self.__berechne_geschuetzte_orte(self.__zentren, self.__orte))
		self.__ausserhalb_gebiet_orte = frozenset(
			{} if alles_im_gebiet else self.__berechne_ausserhalb_gebiet_orte(self.__orte)
		)
		self.__loss = 0
		self.__auswerte_ort_abstand()
		if not alles_im_gebiet:
			self.__auswerte_gebiet()

	def __berechne_ausserhalb_gebiet_orte(self, orte: frozenset[TPunkt]) -> set[TPunkt]:
		return {
			o for o in orte
			if not self.__gebiet.ist_drin(o)
		}

	def __berechne_geschuetzte_orte(self, zentren: frozenset[TPunkt],
			orte: frozenset[TPunkt]) -> set[TPunkt]:
		return {
			o for o in orte
			if any(
				self.__berechne_abstand(z, o) <= self.param.schutz_zentrum_bis
				for z in zentren
			)
		}

	def __auswerte_ort_abstand(self):
		zunahe_orte = set()
		# Einteilung in Planquadrate
		planquadrat = {}
		for x, y in self.__orte:
			px = x // self.param.sicher_abstand_ab
			py = y // self.param.sicher_abstand_ab
			p = px, py
			if p not in planquadrat:
				planquadrat[p] = []
			planquadrat[p].append((x, y))
		# Vergleich der Punkte eines jeden Planquadrats mit sich selbst
		# und mit denen der Planquadrate rechts, linksunten, unten, rechtsunten
		# Dies reicht aus, da
		# - sonst keine zu geringen Abstaende vorhanden sein koennen
		# - die Vergleich in eine Richtung fuer jedes Punktepaar benoetigt wird
		#   (also kein Vergleich mit Planquadraten, die links oder zum Teil oben sind)
		kombinationen = []
		for (px, py), orte in planquadrat.items():
			kombinationen.extend(it.combinations(orte, 2))
			kombinationen.extend([
				(o1, o2)
				for o1 in orte
				for p2 in [(px + 1, py), (px, py + 1), (px + 1, py + 1), (px - 1, py + 1)]
				for o2 in (planquadrat[p2] if p2 in planquadrat else [])
			])
		for o1, o2 in kombinationen:
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

	def __set_zu_str(self, name: str, s: set | frozenset) -> str:
		return f'{name}:\n' + '\n'.join(str(z) for z in s)

	# OVERRIDES
	def __str__(self) -> str:
		return '\n\n'.join([
			self.__set_zu_str('Gebiet-Name', {self.__gebiet.hole_name()}),
			self.__set_zu_str('Gesundheitszentren', self.__zentren),
			self.__set_zu_str('Ortschaften', self.__orte),
			self.__set_zu_str('zunahe Ortschaften', self.__zunahe_orte),
			self.__set_zu_str('geschuetzte Ortschaften', self.__geschuetzte_orte),
			self.__set_zu_str('Ortschaften ausserhalb dem Gebiet', self.__ausserhalb_gebiet_orte),
		])

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
