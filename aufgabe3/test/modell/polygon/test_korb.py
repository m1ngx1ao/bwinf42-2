from modell import Polygon, TPunkt

#   01234567
#  
# 0  ***
# 1 // *
# 2 *  *  *
# 3 \\   **
# 4  *****
# 5

def hole_cut():
	return Polygon([
		(40, 30),
		(40, 0),
		(10, 0),
		(10, 10),
		(0, 20),
		(0, 30),
		(10, 40),
		(10, 50),
		(60, 50),
		(60, 40),
		(70, 40),
		(70, 20),
		(60, 20),
		(60, 30),
		(50, 30),
		(50, 40),
		(20, 40),
		(10, 30),
		(10, 20),
		(20, 10),
		(30, 10),
		(30, 30),
		(40, 30),
	])

def test_y_20_wie_durchgangspunkte_links():
	cut = hole_cut()
	assert cut.enthaelt((5, 20))
	assert not cut.enthaelt((15, 20))
	assert cut.enthaelt((35, 20))

def test_y_30_wie_sattelpunkt_rechts():
	cut = hole_cut()
	assert not cut.enthaelt((15, 30))
	assert not cut.enthaelt((45, 30))
	assert cut.enthaelt((65, 30))

def test_y_40_wie_horizontaler_rand_unten():
	cut = hole_cut()
	assert cut.enthaelt((15, 40))
	assert cut.enthaelt((55, 40))
	assert not cut.enthaelt((75, 40))
