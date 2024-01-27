from abc import ABC, abstractmethod

from modell import Besiedlungsplan

class Beobachter(ABC):
	@abstractmethod
	def melde(self, b: Besiedlungsplan):
		...
