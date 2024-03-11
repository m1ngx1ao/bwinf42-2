import itertools as it
from .besiedlungsplan import TPunkt

class Gebiet:
	def __init__(self, linienzug: list[TPunkt]):
		assert linienzug[0] == linienzug[-1]
		self.__linienzug = linienzug

	def ist_drin(self, p: TPunkt):
		"""
		Implementiert die Strahlmethode (von links) fuer den Punkt-in-Polygon-Test.
		Alle Schnittpunkte des Polygons mit einem horizontalen Strahl von aussen bis zum
		Testpunkt (Px/Py) werden gefunden. Der Punkt liegt im Polygon genau dann wenn
		diese Zahl ungerade ist.

		Um Probleme zu umgehen bei Linienzugspunkten (Lx/Ly) mit Ly == Py,
		werden sie so behandelt, als ob ihre y-Koordinate Ly - ε betraegt:
		Also Ly - ε < Py, was aequivalent zu Ly <= Py ist

		Diese Methode wird zum Beispiel hier aufgefuehrt
			"... considering vertices on the ray as lying slightly above the ray."
			(https://en.wikipedia.org/wiki/Point_in_polygon#Limited_precision)
		
		Die gegebenen Gebiete werden in diesem Sinne interpretiert, d.h. Punkte am oberen Rand
		des Gebiets gehoeren zu ihm, waehrend die auf dem unteren Rand dies nicht tun.
		"""
		px, py = p
		war_groesser = self.__linienzug[0][1] > py
		anzahl_schnittpunkte = 0
		for (lvx, lvy), (lx, ly) in it.pairwise(self.__linienzug):
			if war_groesser != (ly > py):
				war_groesser = not war_groesser
				if ly == py:
					sx = lx
				else:
					sx = lvx + (lx - lvx) * (py - lvy) / (ly - lvy)
				if sx < px:
					anzahl_schnittpunkte += 1
		return anzahl_schnittpunkte % 2 == 1
