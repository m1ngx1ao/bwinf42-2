from modell import Besiedlungsplan

from .beobachter import Beobachter

class Logger(Beobachter):
	def __ausgabe_f(self, s: str):
		print(s)
		self.__f.write(f'{s}\n')

	def optimierer_start(self, b: Besiedlungsplan, strategie: str, system: str):
		self.__iter_num = 0
		pfad_name = super()._vorbereite_output_file_opt(b, strategie, system, 'log.txt')
		self.__f = open(pfad_name, 'w')

	def optimierer_iteration(self, b: Besiedlungsplan):
		self.__iter_num += 1
		self.__ausgabe_f(f'Iteration {self.__iter_num}:')
		self.__ausgabe_f(f'# Gesundheitszentren: {len(b.hole_zentren())}')
		self.__ausgabe_f(f'# Ortschaften: {len(b.hole_orte())}')
		self.__ausgabe_f(f'# zu nahe Ortschaften: {len(b.hole_zunahe_orte())}')
		self.__ausgabe_f(f'# Ortschaften ausserhalb Gebiet: {len(b.hole_ausserhalb_gebiet_orte())}')
		self.__ausgabe_f(f'Loss: {b.hole_loss()}')
		self.__ausgabe_f('')
		
	def optimierer_ende(self):
		self.__f.close()

	def lauf_start(self, b: Besiedlungsplan, strategie: str, system: str):
		self.__pfad_name = super()._vorbereite_output_folder_lauf(b, strategie, system, 'plaene')

	def lauf_loesung(self, b: Besiedlungsplan, iter_num_letzte: int):
		# output/siedler1/gierig/lauf/plaene/20.txt
		with open(f'{self.__pfad_name}/{len(b.hole_orte())}.txt', 'w') as h:
			h.write(str(b))
			h.close()

	def lauf_ende(self):
		...
