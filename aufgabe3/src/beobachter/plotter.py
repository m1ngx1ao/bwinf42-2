import tkinter as tk
import os
from PIL import Image

from modell import Besiedlungsplan, TPunkt
from .beobachter import Beobachter

class Trafo:
	"""
	Nimmt die Punkte des Besiedlungsplans (Ortschaften, Zentren, Gebietseckpunkte)
	und berechnet basierend auf der Canvas-Groesse eine Transformation ("Trafo"),
	welche die Punktkoordinaten so normalisiert, dass die Canvas genau vollstaendig
	ausgenutzt wird.
	"""
	def __init__(self, punkte: frozenset[TPunkt],
			rand: float, breite: float, hoehe: float):
		xs, ys = zip(*punkte)
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

	def __init__(self):
		self.__fenster = tk.Tk()
		breite = Plotter.BREITE + Plotter.RAND * 2
		hoehe = Plotter.HOEHE + Plotter.RAND * 2
		self.__fenster.geometry(f'{ breite }x{ hoehe }')
		self.__canvas = tk.Canvas(self.__fenster, width=breite, height=hoehe)
		self.__canvas.pack()

	# OPTIMIERER

	def optimierer_start(self, plan: Besiedlungsplan, strategie: str):
		self.__iter_num = 0
		self.__pfad_opt = super()._vorbereite_output_folder(
			plan, strategie, self.MODUL_OPTIMIERER, 'karten')

	def optimierer_iteration(self, plan: Besiedlungsplan):
		self.__iter_num += 1
		self.__male(plan)
		self.__speichere_canvas_zu_file(self.__pfad_opt, self.__iter_num)

	def optimierer_ende(self):
		...

	# LAUF

	def lauf_start(self, plan: Besiedlungsplan, strategie: str):
		self.__pfad_lauf = super()._vorbereite_output_folder(
			plan, strategie, self.MODUL_LAUF, 'karten')

	def lauf_loesung(self, plan: Besiedlungsplan, benoetigte_iter_num: int):
		# z.B. output/siedler1/gierig/lauf/karten/20.png
		self.__male(plan)
		self.__speichere_canvas_zu_file(self.__pfad_lauf, len(plan.hole_orte()))

	def lauf_ende(self):
		#self.__fenster.mainloop()
		...

	# PRIVATE

	def __male(self, plan: Besiedlungsplan):
		"""
		Der Plan wird normalisiert gemalt, d.h.
		der linkeste (oberste) Punkt ist
		ist auf dem Schaubild links (oben) abgebildet,
		entsprechend dasselbe fuer rechts und unten.
		"""
		self.__canvas.delete('all')
		trafo = Trafo(
			plan.hole_gebiet().hole_eckpunkte() | plan.hole_orte() | plan.hole_zentren(),
			Plotter.RAND, Plotter.BREITE, Plotter.HOEHE
		)
		self.__male_gebiet(trafo, plan)
		self.__male_zentren(trafo, plan)
		self.__male_orte(trafo, plan)
		self.__fenster.update()

	def __male_gebiet(self, trafo: Trafo, plan: Besiedlungsplan):
		xy_paare = []
		for x, y in plan.hole_gebiet().hole_linienzug():
			xy_paare.append(trafo.x(x))
			xy_paare.append(trafo.y(y))
		self.__canvas.create_polygon(*xy_paare, fill=Plotter.GEBIET_FARBE)

	def __male_zentren(self, trafo: Trafo, plan: Besiedlungsplan):
		for x, y in plan.hole_zentren():
			trafo_x = trafo.x(x)
			trafo_y = trafo.y(y)
			trafo_radius_x = trafo.zoom_x * plan.param.schutz_zentrum_bis
			trafo_radius_y = trafo.zoom_y * plan.param.schutz_zentrum_bis
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

	def __male_orte(self, trafo: Trafo, plan: Besiedlungsplan):
		for o in plan.hole_orte():
			if o in plan.hole_zunahe_orte():
				if o in plan.hole_geschuetzte_orte():
					innen = Plotter.ORTSCHAFT_FARBE_ZUNAHE_MIT_SCHUTZ
				else:
					innen = Plotter.ORTSCHAFT_FARBE_ZUNAHE_OHNE_SCHUTZ
			else:
				innen = Plotter.ORTSCHAFT_FARBE_GUELTIG
			if o in plan.hole_ausserhalb_gebiet_orte():
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

	def __speichere_canvas_zu_file(self, pfad_name: str, index: int):
		eps_name = f'{ pfad_name }.eps'
		self.__canvas.postscript(file = eps_name)
		png_name = ('00' + str(index))[-3:]
		Image.open(eps_name).save(f'{pfad_name}/{png_name}.png', 'png')
		os.remove(eps_name)
