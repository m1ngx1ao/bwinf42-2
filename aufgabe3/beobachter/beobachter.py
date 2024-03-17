import os
import shutil
from abc import ABC, abstractmethod

from modell import Besiedlungsplan

class Beobachter(ABC):
	MODUL_LAUF = 'lauf'
	MODUL_OPTIMIERER = 'optimierer'

	@abstractmethod
	def optimierer_start(self, plan: Besiedlungsplan, strategie: str):
		...
	
	@abstractmethod
	def optimierer_iteration(self, plan: Besiedlungsplan):
		...

	@abstractmethod
	def optimierer_ende(self):
		...

	@abstractmethod
	def lauf_start(self, plan: Besiedlungsplan, strategie: str):
		...

	@abstractmethod
	def lauf_loesung(self, plan: Besiedlungsplan, benoetigte_iter_num: int):
		...

	@abstractmethod
	def lauf_ende(self):
		...
	
	# PROTECTED

	def _vorbereite_output_file(self, plan: Besiedlungsplan, strategie: str,\
			modul: str, file_name: str) -> str:
		pfad = self.__garantiere_folder(plan, strategie, modul)
		pfad += f'/{file_name}'
		self.__garantiere_kein_file(pfad)
		return pfad
	
	def _vorbereite_output_folder(self, plan: Besiedlungsplan, strategie: str, \
			modul: str, folder_name: str) -> str:
		pfad = self.__garantiere_folder(plan, strategie, modul)
		pfad += f'/{folder_name}'
		self.__garantiere_leeren_folder(pfad)
		return pfad

	# PRIVATE

	def __garantiere_kein_file(self, pfad):
		if os.path.isfile(pfad):
			os.remove(pfad)

	def __garantiere_leeren_folder(self, pfad):
		if os.path.isdir(pfad):
			shutil.rmtree(pfad)
		os.mkdir(pfad)

	def __garantiere_folder(self, plan: Besiedlungsplan, strategie: str, \
			modul: str) -> str:
		pfad = f'output/{plan.hole_gebiet().hole_name()}/{strategie}/{modul}'
		if modul == self.MODUL_OPTIMIERER:
			aufgabe = f'{len(plan.hole_zentren())}/{len(plan.hole_orte())}'
			pfad += f'/{aufgabe}'
		if not os.path.isdir(pfad):
			os.makedirs(pfad)
		return pfad
