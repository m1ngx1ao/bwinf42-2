import tkinter as tk
#from PIL import Image

from modell import Besiedlungsplan, TOrt
from .beobachter import Beobachter

class Trafo:
	def __init__(self, orte: frozenset[TOrt],
			rand: float, breite: float, hoehe: float):
		xs, ys = zip(*orte)
		self.min_x, self.max_x = min(xs), max(xs)
		self.min_y, self.max_y = min(ys), max(ys)
		self.zoom_x = breite / (self.max_x - self.min_x)
		self.zoom_y = hoehe / (self.max_y - self.min_y)
		self.rand = rand
	def x(self, x: float):
		return self.zoom_x * (x - self.min_x) + self.rand
	def y(self, y: float):
		return self.zoom_y * (y - self.min_y) + self.rand

class Plotter(Beobachter):
	BREITE = 500
	HOEHE = 500
	RAND = 7
	ORTSCHAFT_RADIUS = 3
	ORTSCHAFT_FARBE = '#66F'
	#ORTSCHAFT_FARBE_GUELTIG = '#6F6'
	#ORTSCHAFT_FARBE_UNGUELTIG = '#F33'
	ZENTRUM_RADIUS = 3
	ZENTRUM_FARBE = 'black'

	def __init__(self):
		self.__fenster = tk.Tk()
		breite = Plotter.BREITE + Plotter.RAND * 2
		hoehe = Plotter.HOEHE + Plotter.RAND * 2
		self.__fenster.geometry(f'{ breite }x{ hoehe }')
		self.__canvas = tk.Canvas(self.__fenster, width=breite, height=hoehe)
		self.__canvas.pack()

	def melde(self, b: Besiedlungsplan):
		"""
		Normalisiert, das heisst, der linkeste obendste
		Punkt ist auf links oben auf dem Schaubild abgebildet,
		der rechts unteste Punkt ist entsprechend 
		soweit wie moeglich rechts unten auf dem Schaubild abgebildet,
		damit es sich besser anschauen laesst.
		Der Punkt (0,0) befindet sich oben links.
		"""
		trafo = Trafo(
			b.hole_ortschaften() | b.hole_zentren(),
			Plotter.RAND, Plotter.BREITE, Plotter.HOEHE
		)
		self.__male_zentren(trafo, b.hole_zentren(), b.param.schutz_zentrum_bis)
		self.__male_ortschaften(trafo, b.hole_ortschaften())
		self.__fenster.update()
		self.__fenster.mainloop()

	def __male_zentren(self, trafo: Trafo, zentren: frozenset[TOrt], schutz_bis: float):
		for x, y in zentren:
			trafo_x = trafo.x(x)
			trafo_y = trafo.y(y)
			trafo_radius_x = trafo.zoom_x * schutz_bis
			trafo_radius_y = trafo.zoom_y * schutz_bis
			self.__canvas.create_oval(
				trafo_x - trafo_radius_x,
				trafo_y - trafo_radius_y,
				trafo_x + trafo_radius_x,
				trafo_y + trafo_radius_y,
				fill='cyan'
			)
			self.__canvas.create_rectangle(
				trafo_x - Plotter.ZENTRUM_RADIUS,
				trafo_y - Plotter.ZENTRUM_RADIUS,
				trafo_x + Plotter.ZENTRUM_RADIUS,
				trafo_y + Plotter.ZENTRUM_RADIUS,
				fill=Plotter.ZENTRUM_FARBE
			)

	def __male_ortschaften(self, trafo: Trafo, ortschaften: frozenset[TOrt]):
		for x, y in ortschaften:
			trafo_x = trafo.x(x)
			trafo_y = trafo.y(y)
			self.__canvas.create_oval(
				trafo_x - Plotter.ORTSCHAFT_RADIUS,
				trafo_y - Plotter.ORTSCHAFT_RADIUS,
				trafo_x + Plotter.ORTSCHAFT_RADIUS,
				trafo_y + Plotter.ORTSCHAFT_RADIUS,
				fill=Plotter.ORTSCHAFT_FARBE
			)
