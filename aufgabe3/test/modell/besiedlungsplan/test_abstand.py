from modell import Besiedlungsplan
from modell import Parameter

def test_2orte_abstand_10_vertikal_mit_schutz():
	b = Besiedlungsplan({(87, 3), (87, 13)}, {(2, 3)}, Parameter())
	assert not b.hole_zunahe_orte()
	assert b.hole_geschuetzte_orte() == {(87, 3)}
	assert b.hole_loss() == 0

def test_2orte_abstand_10_vertikal_knapp_ausserhalb_schutz():
	b = Besiedlungsplan({(87, -2), (87, 8)}, {(2, 3)}, Parameter())
	assert b.hole_zunahe_orte()
	assert not b.hole_geschuetzte_orte()
	assert b.hole_loss() == 10

def test_2orte_abstand_unter20_ohne_schutz():
	orte = {(0, 0), (4, 19.49)}
	b = Besiedlungsplan(orte, set(), Parameter())
	assert b.hole_zunahe_orte() == orte

def test_2orte_abstand_ueber20_ohne_schutz():
	b = Besiedlungsplan({(0, 0), (200, 200)}, set(), Parameter())
	assert not b.hole_zunahe_orte()

def test_4orte_abstand_unter10_mit_schutz():
	orte = {(0, 0), (0, 9.9), (100, 99), (100, 100)}
	b = Besiedlungsplan(orte, {(0, 0)}, Parameter())
	assert b.hole_zunahe_orte() == orte
	assert 19.1 == b.hole_loss()

def test_5orte_abstand_ueber20_horizontal_mit_schutz():
	b = Besiedlungsplan({(0, 0), (0, 30), (30, 100), (150, 30), (200, 200)}, {(100, 100)}, Parameter())
	assert not b.hole_zunahe_orte()

def test_2orte_abstand_10_mit_ohne_schutz():
	"""
	Wenn der Abstand zwischen 2 Punkten 10 betraegt, sich ein Punkt in der Schutzzone, der andere
	Punkt nicht, befindet, so gibt es kein Problem mit der Krankheitenuebertragung, da
	geschuetzte orte keine Krankheiten uebertragen koennen, somit ist die "nichtgeschuetzte"
	Ortschaft automatisch auch geschuetzt, weil ihr von der anderen nichts uebertragen werden kann.
	"""
	b = Besiedlungsplan({(150, 167.5), (156, 175.5)}, {(100, 100)}, Parameter())
	assert not b.hole_zunahe_orte()
