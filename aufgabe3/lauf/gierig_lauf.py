from random import random

from beobachter import Beobachter
from modell import Besiedlungsplan, Gebiet, Parameter, TPunkt
from optimierung import GierigOptimierer

class GierigLauf:
	STRATEGIE = 'gierig'
	SYSTEM = 'lauf'
	BUDGET_ZENTREN = 0
	BUDGET_MAX_VERSUCHE = 1

	def __init__(self, gebiet_name: str, beobachter: list[Beobachter]):
		self.__gebiet = Gebiet.von_datei(gebiet_name)
		self.__beobachter = beobachter

	def tue(self):
		plan = Besiedlungsplan(
			self.__gebiet,
			set(),
			set(),
			Parameter(),
			alles_im_gebiet=True
		)
		for b in self.__beobachter:
			b.lauf_start(plan, self.STRATEGIE, self.SYSTEM)
		versuche = 0
		anzahl_zentren = 0
		insg_iter_num = 0
		while True:
			if versuche == self.BUDGET_MAX_VERSUCHE:
				# gebe auf, bei aktueller Zentrenzahl die Ortzahl weiter zu steigern
				# fuege stattdessen (wenn erlaubt) noch ein Zentrum hinzu
				if anzahl_zentren == self.BUDGET_MAX_VERSUCHE:
					for b in self.__beobachter:
						b.lauf_ende()
					return
				versuche = 0
				anzahl_zentren += 1
			zentren = plan.hole_zentren()
			# neues Zentrum wird bei jedem Versuch neu gelegt und damit bei fehlendem Erfolg verworfen
			zentren |= {self.__hole_ort(self.__gebiet) for _ in range(anzahl_zentren - len(zentren))}
			kandidat = Besiedlungsplan(
				self.__gebiet,
				{self.__hole_ort(self.__gebiet)} | plan.hole_orte(),
				zentren,
				plan.param,
				alles_im_gebiet=True
			)
			iter_num, optimierter_kandidat = GierigOptimierer(kandidat, self.__beobachter).tue()
			insg_iter_num += iter_num
			if optimierter_kandidat.hole_loss() == 0:
				versuche = 0
				plan = optimierter_kandidat
				for b in self.__beobachter:
					b.lauf_loesung(plan, insg_iter_num)
				insg_iter_num = 0
			else:
				versuche += 1

	def __hole_ort(self, g: Gebiet) -> TPunkt:
		xs, ys = zip(*g.hole_eckpunkte())
		min_x, max_x = min(*xs), max(*xs)
		min_y, max_y = min(*ys), max(*ys)
		while True:
			x = (max_x - min_x) * random() + min_x
			y = (max_y - min_y) * random() + min_y
			if g.ist_drin((x, y)):
				return x, y
