from modell import Polygon, TPunkt

# *\ /*
# *\*/*
# *   * 
# *   * 

def hole_cut():
	return Polygon([
		(0, 0),
		(10, 0),
		(20, 10),
		(30, 0),
		(40, 0),
		(40, 30),
		(30, 30),
		(30, 10),
		(20, 20),
		(10, 10),
		(10, 30),
		(0, 30),
		(0, 0),
	])

def test_hohlraum_draussen():
	cut = hole_cut()
	assert not cut.enthaelt((11, 15))
	assert not cut.enthaelt((29, 15))
	assert not cut.enthaelt((20, 9))
	assert not cut.enthaelt((20, 21))

def test_schraege_drinnen():
	cut = hole_cut()
	assert cut.enthaelt((20, 19))
	assert cut.enthaelt((20, 11))
	assert cut.enthaelt((12, 11))
	assert cut.enthaelt((28, 11))
	assert cut.enthaelt((11, 2))

def test_selbes_y():
	"""
	Bei diesem Polygon gibt es v-foermige (bzw. gross-Lambda-foermige) Ecken.
	Deren y-Koordinaten werden an anderen x-Koordinaten getestet.
	"""
	cut = hole_cut()
	assert cut.enthaelt((11, 10))
	assert cut.enthaelt((29, 10))
	assert cut.enthaelt((19, 10))
	assert cut.enthaelt((21, 10))
	assert cut.enthaelt((5, 20))
	assert cut.enthaelt((25, 20))
	assert not cut.enthaelt((21, 20))
	assert not cut.enthaelt((19, 20))
	assert not cut.enthaelt((11, 0))
	assert not cut.enthaelt((29, 0))
