from modell import Besiedlungsplan

from .beobachter import Beobachter

class Stats(Beobachter):
	def __ausgabe(self, l: list[str | float | int]):
		self.__f.write(','.join(str(e) for e in l) + '\n')

	def __init__(self, lauf_name: str):
		self.__iter_num = 0
		pfad = super()._vorbereite_output_file(lauf_name, 'stats.csv')
		self.__f = open(pfad, 'w')
		self.__ausgabe([
			'Iteration',
			'Loss',
			'#OrtschaftenZuNah',
			'#OrtschaftenNichtImGebiet',
			'#Ortschaften',
			'#Gesundheitszentren'
		])

	def melde(self, b: Besiedlungsplan):
		self.__iter_num += 1
		self.__ausgabe([
			self.__iter_num,
			b.hole_loss(),
			len(b.hole_zunahe_orte()),
			0, #len(b.hole_orte_nicht_im_gebiet())
			len(b.hole_orte()),
			len(b.hole_zentren())
		])
		
	def finalisiere(self):
		self.__f.close()