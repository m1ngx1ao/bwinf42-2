from modell import Besiedlungsplan

from .beobachter import Beobachter

class Logger(Beobachter):
	def __ausgabe(self, s: str):
		print(s)
		self.__f.write(f'{s}\n')

	# OPTIMIERER
		
	def optimierer_start(self, plan: Besiedlungsplan, strategie: str):
		self.__iter_num = 0
		pfad = super()._vorbereite_output_file(plan, strategie, self.MODUL_OPTIMIERER, 'log.txt')
		self.__f = open(pfad, 'w')

	def optimierer_iteration(self, plan: Besiedlungsplan):
		self.__iter_num += 1
		self.__ausgabe(f'Iteration {self.__iter_num}:')
		self.__ausgabe(f'# Gesundheitszentren: {len(plan.hole_zentren())}')
		self.__ausgabe(f'# Ortschaften: {len(plan.hole_orte())}')
		self.__ausgabe(f'# zu nahe Ortschaften: {len(plan.hole_zunahe_orte())}')
		self.__ausgabe(f'# Ortschaften ausserhalb Gebiet: {len(plan.hole_ausserhalb_gebiet_orte())}')
		self.__ausgabe(f'Loss: {plan.hole_loss()}')
		self.__ausgabe('')
		
	def optimierer_ende(self):
		self.__f.close()

	# LAUF
		
	def lauf_start(self, plan: Besiedlungsplan, strategie: str):
		# z.B. output/siedler1/gierig/lauf/plandaten/20.txt
		self.__lauf_pfad = super()._vorbereite_output_folder(
			plan, strategie, self.MODUL_LAUF, 'plandaten')

	def lauf_loesung(self, plan: Besiedlungsplan, benoetigte_iter_num: int):
		with open(f'{self.__lauf_pfad}/{len(plan.hole_orte())}.txt', 'w') as f:
			f.write(str(plan))
			f.close()

	def lauf_ende(self):
		...
