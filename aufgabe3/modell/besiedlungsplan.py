from .parameter import Parameter

TOrt = tuple[float, float]

class Besiedlungsplan:
	def __init__(self, ortschaften: set[TOrt],
			zentren: set[TOrt], param: Parameter):
		self.__ortschaften = frozenset(ortschaften)
		self.__zentren = frozenset(zentren)
		self.param = param

	def hole_ortschaften(self):
		return self.__ortschaften

	def hole_zentren(self):
		return self.__zentren
