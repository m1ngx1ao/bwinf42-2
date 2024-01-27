from modell import Besiedlungsplan
from modell import Parameter
from ausgabe import Plotter

class GierigLauf:
	def tue(self):
		b = Besiedlungsplan(
			{
				(0, 0),
				(0, 50),
				(100, 5),
				(150, 50),
				(150, 80)
			},
			{(200, 100)},
			Parameter()
		)
		Plotter().melde(b)
