import io

from modell import Besiedlungsplan

from .beobachter import Beobachter

class Stats(Beobachter):
	def __ausgabe(self, l: list[str | float | int], ort: io.TextIOWrapper):
		ort.write(','.join(str(e) for e in l) + '\n')

	# OPTIMIERER
		
	def optimierer_start(self, plan: Besiedlungsplan, strategie: str):
		self.__iter_num = 0
		pfad = super()._vorbereite_output_file(plan, strategie, self.MODUL_OPTIMIERER, 'stats.csv')
		self.__f_opt = open(pfad, 'w')
		self.__ausgabe([
			'Iteration',
			'Loss',
			'#OrtschaftenZuNah',
			'#OrtschaftenNichtImGebiet',
			'#Ortschaften',
			'#Gesundheitszentren'
		], self.__f_opt)

	def optimierer_iteration(self, plan: Besiedlungsplan):
		self.__iter_num += 1
		self.__ausgabe([
			self.__iter_num,
			plan.hole_loss(),
			len(plan.hole_zunahe_orte()),
			len(plan.hole_ausserhalb_gebiet_orte()),
			len(plan.hole_orte()),
			len(plan.hole_zentren())
		], self.__f_opt)
		
	def optimierer_ende(self):
		self.__f_opt.close()
	
	# LAUF

	def lauf_start(self, plan: Besiedlungsplan, strategie: str):
		# z.B. output/siedler2/gierig/lauf/stats.csv
		pfad = super()._vorbereite_output_file(plan, strategie, self.MODUL_LAUF, 'stats.csv')
		self.__f_lauf = open(pfad, 'w')
		self.__ausgabe([
			'#Ortschaften',
			'#Gesundheitszentren',
			'#BenoetigteIterationen'
		], self.__f_lauf)

	def lauf_loesung(self, plan: Besiedlungsplan, benoetigte_iter_num: int):
		self.__ausgabe([
			len(plan.hole_orte()),
			len(plan.hole_zentren()),
			benoetigte_iter_num
		], self.__f_lauf)

	def lauf_ende(self):
		self.__f_lauf.close()
