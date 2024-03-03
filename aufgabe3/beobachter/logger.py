from modell import Besiedlungsplan

from .beobachter import Beobachter

class Logger(Beobachter):
	def __init__(self, lauf_name: str):
		self.__iter_num = 0
		pfad_name = super()._vorbereite_output_file(lauf_name, 'log.txt')
		self.__f = open(pfad_name, 'w')

	def __ausgabe(self, s: str):
		print(s)
		self.__f.write(f'{s}\n')

	def melde(self, b: Besiedlungsplan):
		self.__iter_num += 1
		self.__ausgabe(f'Iteration {self.__iter_num}:')
		self.__ausgabe(f'# Gesundheitszentren: {len(b.hole_zentren())}')
		self.__ausgabe(f'# Ortschaften: {len(b.hole_orte())}')
		self.__ausgabe(f'# zunahen Ortschaften: {len(b.hole_zunahe_orte())}')
		self.__ausgabe(f'Loss: {b.hole_loss()}')
		self.__ausgabe('')
		
	def finalisiere(self):
		self.__f.close()