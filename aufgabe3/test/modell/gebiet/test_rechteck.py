from modell import Gebiet

def hole_cut():
	return Gebiet([
		(0, 0),
		(20, 0),
		(20, 10),
		(0, 10),
		(0, 0),
	])

def test_draussen():
	cut = hole_cut()
	assert not cut.ist_drin((5, -1))
	assert not cut.ist_drin((5, 11))
	assert not cut.ist_drin((-1, 5))
	assert not cut.ist_drin((21, 5))

def test_drinnen():
	cut = hole_cut()
	assert cut.ist_drin((1, 1))
	assert cut.ist_drin((19, 9))
