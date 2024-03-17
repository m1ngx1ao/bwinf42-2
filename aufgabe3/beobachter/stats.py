import io

from modell import Besiedlungsplan

from .beobachter import Beobachter

class Stats(Beobachter):
	def __ausgabe(self, l: list[str | float | int], ort: io.TextIOWrapper):
		ort.write(','.join(str(e) for e in l) + '\n')

	def optimierer_start(self, b: Besiedlungsplan, strategie: str, system: str):
		self.__iter_num = 0
		pfad = super()._vorbereite_output_file_opt(b, strategie, system, 'stats.csv')
		self.__f = open(pfad, 'w')
		self.__ausgabe([
			'Iteration',
			'Loss',
			'#OrtschaftenZuNah',
			'#OrtschaftenNichtImGebiet',
			'#Ortschaften',
			'#Gesundheitszentren'
		], self.__f)

	def optimierer_iteration(self, b: Besiedlungsplan):
		self.__iter_num += 1
		self.__ausgabe([
			self.__iter_num,
			b.hole_loss(),
			len(b.hole_zunahe_orte()),
			len(b.hole_ausserhalb_gebiet_orte()),
			len(b.hole_orte()),
			len(b.hole_zentren())
		], self.__f)
		
	def optimierer_ende(self):
		self.__f.close()
	
	def lauf_start(self, b: Besiedlungsplan, strategie: str, system: str):
		# output/siedler/gierig/lauf/stats.csv
		pfad = super()._vorbereite_output_file_lauf(b, strategie, system, 'stats.csv')
		self.__h = open(pfad, 'w')
		self.__ausgabe([
			'#Ortschaften',
			'#Gesundheitszentren',
			'benoetigte Iterationen fuer letzten Plan'
		], self.__h)

	def lauf_loesung(self, b: Besiedlungsplan, iter_num_letzte: int):
		self.__ausgabe([
			len(b.hole_orte()),
			len(b.hole_zentren()),
			iter_num_letzte
		], self.__h)

	def lauf_ende(self):
		self.__h.close()
