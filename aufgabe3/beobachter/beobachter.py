import os
import shutil
from abc import ABC, abstractmethod

from modell import Besiedlungsplan

class Beobachter(ABC):
	@abstractmethod
	def melde(self, b: Besiedlungsplan):
		...

	@abstractmethod
	def finalisiere(self):
		...
	
	def __vorbereite_output(self, lauf_name: str) -> str:
		pfad = f'output/{lauf_name}'
		if not os.path.isdir(pfad):
			os.mkdir(pfad)
		return pfad
	
	def _vorbereite_output_file(self, lauf_name: str, file_name: str) -> str:
		pfad_lauf = self.__vorbereite_output(lauf_name)
		pfad = f'{pfad_lauf}/{file_name}'
		if os.path.isfile(pfad):
			os.remove(pfad)
		return pfad
	
	def _vorbereite_output_folder(self, lauf_name: str, folder_name: str) -> str:
		pfad_lauf = self.__vorbereite_output(lauf_name)
		pfad = f'{pfad_lauf}/{folder_name}'
		if os.path.isdir(pfad):
			shutil.rmtree(pfad)
			os.mkdir(pfad)
		return pfad
