package test.modell;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

import modell.Schulhof;

class SchulhofBasisTest {
	Schulhof cut;

	@Test
	void konstruierePerGroesseUeberallStandardMenge() {
		cut = new Schulhof(3, 2);
		assertEquals(100, cut.holeLaub(0, 1));
		assertEquals(100, cut.holeLaub(1, 1));
	}

	@Test
	void konstruierePerMatrixUebernommen() {
		cut = new Schulhof(4, 2, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8
		});
		assertEquals(2, cut.holeLaub(1, 0));
		assertEquals(8, cut.holeLaub(3, 1));
	}

	@Test
	void zuText5m3() {
		cut = new Schulhof(5, 3);
		String exp = """
		--------------------------
		| 100| 100| 100| 100| 100|
		--------------------------
		| 100| 100| 100| 100| 100|
		--------------------------
		| 100| 100| 100| 100| 100|
		--------------------------""";
	
		assertEquals(exp, cut.toString());
	}

	@Test
	void zuText3m2() {
		cut = new Schulhof(3, 2);
		String exp = """
		----------------
		| 100| 100| 100|
		----------------
		| 100| 100| 100|
		----------------""";
		assertEquals(exp, cut.toString());
	}
}
