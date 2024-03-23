from random import random

from beobachter import Beobachter
from modell import Besiedlungsplan, Gebiet, Parameter, TPunkt
from optimierung import GierigOptimierer

class GierigLauf:
	STRATEGIE = 'gierig'
	BUDGET_MAX_LAUF_ITER = 80

	def __init__(self, gebiet_name: str, beobachter: list[Beobachter],
			param: Parameter, budget_zentren: int = 3):
		self.__gebiet = Gebiet.von_datei(gebiet_name)
		self.__beobachter = beobachter
		self.__param = param
		self.__budget_zentren = budget_zentren

	def tue(self):
		plan = Besiedlungsplan(
			self.__gebiet,
			set(),
			set(),
			self.__param,
			alles_im_gebiet=True
		)
		for b in self.__beobachter:
			b.lauf_start(plan, self.STRATEGIE)
		sollanzahl_zentren = len(plan.hole_zentren())
		lauf_iter_num = 0
		insg_opt_iter_num = 0
		while True:
			if lauf_iter_num == self.BUDGET_MAX_LAUF_ITER:
				# gebe auf, bei aktueller Zentrenzahl die Ortzahl weiter zu steigern
				# fuege stattdessen (wenn erlaubt) noch ein Zentrum hinzu
				if sollanzahl_zentren == self.__budget_zentren:
					for b in self.__beobachter:
						b.lauf_ende()
					return
				lauf_iter_num = 0
				sollanzahl_zentren += 1
			zentren = plan.hole_zentren()
			# fehlt Zentrum wird es bei jeder Lauf-Iteration neu gelegt
			# und damit bei fehlendem Erfolg verworfen
			zentren |= {
				self.__gebiet.zufaelliger_punkt()
				for _ in range(sollanzahl_zentren - len(zentren))
			}
			lauf_iter_num += 1
			kandidat = Besiedlungsplan(
				self.__gebiet,
				{self.__gebiet.zufaelliger_punkt()} | plan.hole_orte(),
				zentren,
				self.__param,
				alles_im_gebiet=True
			)
			if kandidat.hole_loss() > 0:
				opt_iter_num, kandidat = GierigOptimierer(kandidat, self.__beobachter).tue()
				insg_opt_iter_num += opt_iter_num
			if kandidat.hole_loss() == 0:
				lauf_iter_num = 0
				plan = kandidat
				for b in self.__beobachter:
					b.lauf_loesung(plan, insg_opt_iter_num)
				insg_opt_iter_num = 0
