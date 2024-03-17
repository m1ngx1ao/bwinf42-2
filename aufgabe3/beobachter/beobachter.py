import os
import shutil
from abc import ABC, abstractmethod

from modell import Besiedlungsplan

class Beobachter(ABC):

	@abstractmethod
	def optimierer_iteration(self, b: Besiedlungsplan):
		...

	@abstractmethod
	def optimierer_start(self, b: Besiedlungsplan, strategie: str, system: str):
		...
	
	@abstractmethod
	def optimierer_ende(self):
		...

	@abstractmethod
	def lauf_start(self, b: Besiedlungsplan, strategie: str, system: str):
		...

	@abstractmethod
	def lauf_loesung(self, b: Besiedlungsplan, iter_num_letzte: int):
		...

	@abstractmethod
	def lauf_ende(self):
		...
	
	def __vorbereite_output_opt(self, b: Besiedlungsplan, strategie: str, system: str) -> str:
		# z.B. output/siedler1/gierig/optimierer/1/25
		aufgabe = f'{len(b.hole_zentren())}/{len(b.hole_orte())}'
		return self.__vorbereite_verzeichnis_output(b, strategie, system, aufgabe=aufgabe)

	def _vorbereite_output_file_opt(self, b: Besiedlungsplan, strategie: str,\
			system: str, file_name: str) -> str:
		pfad_lauf = self.__vorbereite_output_opt(b, strategie, system)
		pfad = f'{pfad_lauf}/{file_name}'
		self.__vorbereite_file(pfad)
		return pfad
	
	def _vorbereite_output_folder_opt(self, b: Besiedlungsplan, strategie: str, \
			system: str, folder_name: str) -> str:
		pfad_lauf = self.__vorbereite_output_opt(b, strategie, system)
		pfad = f'{pfad_lauf}/{folder_name}'
		self.__vorbereite_folder(pfad)
		return pfad

	def __vorbereite_verzeichnis_output(self, b: Besiedlungsplan, strategie: str, \
			system: str, aufgabe: str|None) -> str:
		pfad = f'output/{b.hole_gebiet().hole_name()}/{strategie}/{system}'
		if aufgabe:
			pfad += f'/{aufgabe}'
		if not os.path.isdir(pfad):
			os.makedirs(pfad)
		return pfad

	def _vorbereite_output_file_lauf(self, b: Besiedlungsplan, strategie: str,\
			system: str, file_name: str) -> str:
		pfad = self.__vorbereite_pfad_name_lauf(b, strategie, system, file_name)
		self.__vorbereite_file(pfad)
		return pfad
	
	def _vorbereite_output_folder_lauf(self, b: Besiedlungsplan, strategie: str, \
			system: str, folder_name: str) -> str:
		pfad = self.__vorbereite_pfad_name_lauf(b, strategie, system, folder_name)
		self.__vorbereite_folder(pfad)
		return pfad

	def __vorbereite_pfad_name_lauf(self, b: Besiedlungsplan, \
			strategie: str, system: str, name: str) -> str:
		pfad_lauf = self.__vorbereite_verzeichnis_output(b, strategie, system, aufgabe=None)
		return f'{pfad_lauf}/{name}'

	def __vorbereite_folder(self, pfad):
		if os.path.isdir(pfad):
			shutil.rmtree(pfad)
		os.mkdir(pfad)

	def __vorbereite_file(self, pfad):
		if os.path.isfile(pfad):
			os.remove(pfad)
