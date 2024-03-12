import tkinter as tk
import os
from PIL import Image

from modell import Besiedlungsplan, TPunkt
from .beobachter import Beobachter

class Trafo:
	def __init__(self, orte: frozenset[TPunkt],
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
	GEBIET_FARBE = '#CCC'
	ORTSCHAFT_RADIUS = 3
	ORTSCHAFT_FARBE_GUELTIG = '#6F6'
	ORTSCHAFT_FARBE_ZUNAHE_MIT_SCHUTZ = '#66F'
	ORTSCHAFT_FARBE_ZUNAHE_OHNE_SCHUTZ = '#F3F'
	ORTSCHAFT_RAND_AUSSERHALB_GEBIET = '#F00'
	ORTSCHAFT_RAND_IM_GEBIET = '#000'
	ZENTRUM_RADIUS = 3
	ZENTRUM_FARBE = 'black'

	def __init__(self, lauf_name):
		self.__fenster = tk.Tk()
		self.__pfad_name = super()._vorbereite_output_folder(lauf_name, 'karten')
		breite = Plotter.BREITE + Plotter.RAND * 2
		hoehe = Plotter.HOEHE + Plotter.RAND * 2
		self.__iter_num = 0
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
		self.__iter_num += 1
		self.__canvas.delete('all')
		trafo = Trafo(
			b.hole_gebiet().hole_eckpunkte() | b.hole_orte() | b.hole_zentren(),
			Plotter.RAND, Plotter.BREITE, Plotter.HOEHE
		)
		self.__male_gebiet(trafo, b)
		self.__male_zentren(trafo, b)
		self.__male_orte(trafo, b)
		self.__fenster.update()
		self.__speichere_canvas_to_file(self.__pfad_name, self.__iter_num)

	def finalisiere(self):
		#self.__fenster.mainloop()
		...

	def __male_gebiet(self, trafo: Trafo, b: Besiedlungsplan):
		xy_paare = []
		for x, y in b.hole_gebiet().hole_linienzug():
			xy_paare.append(trafo.x(x))
			xy_paare.append(trafo.y(y))
		self.__canvas.create_polygon(*xy_paare, fill=Plotter.GEBIET_FARBE)

	def __male_zentren(self, trafo: Trafo, b: Besiedlungsplan):
		for x, y in b.hole_zentren():
			trafo_x = trafo.x(x)
			trafo_y = trafo.y(y)
			trafo_radius_x = trafo.zoom_x * b.param.schutz_zentrum_bis
			trafo_radius_y = trafo.zoom_y * b.param.schutz_zentrum_bis
			self.__canvas.create_oval(
				trafo_x - trafo_radius_x,
				trafo_y - trafo_radius_y,
				trafo_x + trafo_radius_x,
				trafo_y + trafo_radius_y
			)
			self.__canvas.create_rectangle(
				trafo_x - Plotter.ZENTRUM_RADIUS,
				trafo_y - Plotter.ZENTRUM_RADIUS,
				trafo_x + Plotter.ZENTRUM_RADIUS,
				trafo_y + Plotter.ZENTRUM_RADIUS,
				fill=Plotter.ZENTRUM_FARBE
			)

	def __male_orte(self, trafo: Trafo, b: Besiedlungsplan):
		for o in b.hole_orte():
			if o in b.hole_zunahe_orte():
				if o in b.hole_geschuetzte_orte():
					innen = Plotter.ORTSCHAFT_FARBE_ZUNAHE_MIT_SCHUTZ
				else:
					innen = Plotter.ORTSCHAFT_FARBE_ZUNAHE_OHNE_SCHUTZ
			else:
				innen = Plotter.ORTSCHAFT_FARBE_GUELTIG
			if o in b.hole_ausserhalb_gebiet_orte():
				rand = Plotter.ORTSCHAFT_RAND_AUSSERHALB_GEBIET
			else:
				rand = Plotter.ORTSCHAFT_RAND_IM_GEBIET
			x, y = o
			trafo_x = trafo.x(x)
			trafo_y = trafo.y(y)
			self.__canvas.create_oval(
				trafo_x - Plotter.ORTSCHAFT_RADIUS,
				trafo_y - Plotter.ORTSCHAFT_RADIUS,
				trafo_x + Plotter.ORTSCHAFT_RADIUS,
				trafo_y + Plotter.ORTSCHAFT_RADIUS,
				fill=innen,
				outline=rand
			)

	def __speichere_canvas_to_file(self, pfad_name: str, iter_num: int):
		eps_name = f'{ pfad_name }.eps'
		self.__canvas.postscript(file = eps_name)
		png_name = ('0000' + str(iter_num))[-5:]
		Image.open(eps_name).save(f'{pfad_name}/{png_name}.png', 'png')
		os.remove(eps_name)
