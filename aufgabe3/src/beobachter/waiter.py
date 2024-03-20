import time

from modell import Besiedlungsplan

from .beobachter import Beobachter

class Waiter(Beobachter):
	def __init__(self, sleep_dauer: float):
		self.__sleep_dauer = sleep_dauer
	def optimierer_iteration(self, _: Besiedlungsplan):
		print('waiting after iteration')
		time.sleep(self.__sleep_dauer)
	def optimierer_ende(self):
		print('finalized')
