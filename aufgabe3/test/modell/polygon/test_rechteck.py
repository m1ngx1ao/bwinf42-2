from modell import Polygon, TPunkt

def hole_cut():
	return Polygon([
		(0, 0),
		(20, 0),
		(20, 10),
		(0, 10),
		(0, 0),
	])

def test_draussen():
	cut = hole_cut()
	assert not cut.enthaelt((5, -1))
	assert not cut.enthaelt((5, 11))
	assert not cut.enthaelt((-1, 5))
	assert not cut.enthaelt((21, 5))

def test_drinnen():
	cut = hole_cut()
	assert cut.enthaelt((1, 1))
	assert cut.enthaelt((19, 9))
