from modell import Gebiet

# *\/*
# *\/*
# *  * 
# *  * 

def hole_cut():
	return Gebiet([
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
	assert not cut.ist_drin((11, 15))
	assert not cut.ist_drin((29, 15))
	assert not cut.ist_drin((20, 9))
	assert not cut.ist_drin((20, 21))

def test_schraege_drinnen():
	cut = hole_cut()
	assert cut.ist_drin((20, 19))
	assert cut.ist_drin((20, 11))
	assert cut.ist_drin((12, 11))
	assert cut.ist_drin((28, 11))
	assert cut.ist_drin((11, 2))

def test_selbes_y():
	"""
	Bei diesem Polygon gibt es v-foermige (bzw. gross-Lambda-foermige) Ecken.
	Deren y-Koordinaten werden an anderen x-Koordinaten getestet.
	"""
	cut = hole_cut()
	assert cut.ist_drin((11, 10))
	assert cut.ist_drin((29, 10))
	assert cut.ist_drin((19, 10))
	assert cut.ist_drin((21, 10))
	assert cut.ist_drin((5, 20))
	assert not cut.ist_drin((25, 20))
	assert not cut.ist_drin((21, 20))
	assert not cut.ist_drin((19, 20))
	assert not cut.ist_drin((11, 0))
	assert not cut.ist_drin((29, 0))
