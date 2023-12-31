package test.modell;
import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import modell.Feld;
import modell.Schulhof;

public class SchulhofRechteckAequivalenzTest {
	Schulhof cut;

	@BeforeEach
	void setUp() {
		cut = new Schulhof(4, 3, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 11, 12
		}, null);
	}
	
	@Test
	void negativBeispiel() {
		Schulhof keineSpiegelung = new Schulhof(4, 3, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 11, 10, 12
		}, null);
		assertNotEquals(cut, keineSpiegelung);
	}
	
	@Test
	void vertikal() {
		Schulhof spiegelung = new Schulhof(4, 3, new int[] {
			9, 10, 11, 12,
			5, 6, 7, 8,
			1, 2, 3, 4
		}, null);
		assertEquals(cut, spiegelung);
	}
	
	@Test
	void horizontal() {
		Schulhof spiegelung = new Schulhof(4, 3, new int[] {
			4, 3, 2, 1,
			8, 7, 6, 5,
			12, 11, 10, 9
		}, null);
		assertEquals(cut, spiegelung);
	}
	
	@Test
	void diagonalZaehltNichtDaGroessenveraenderung() {
		Schulhof spiegelung = new Schulhof(3, 4, new int[] {
			1, 5, 9,
			2, 6, 10,
			3, 7, 11,
			4, 8, 12
		}, null);
		assertNotEquals(cut, spiegelung);
	}
	
	@Test
	void alleSpiegelungen() {
		Schulhof spiegelung = new Schulhof(4, 3, new int[] {
			12, 11, 10, 9,
			8, 7, 6, 5,
			4, 3, 2, 1
		}, null);
		assertEquals(cut, spiegelung);
	}
	
	@Test
	void horizontalSpiegelungMitZielfeld() {
		cut = new Schulhof(4, 3, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 11, 12
		}, new Feld(1, 1));
		Schulhof spiegelung = new Schulhof(4, 3, new int[] {
			4, 3, 2, 1,
			8, 7, 6, 5,
			12, 11, 10, 9
		}, new Feld(2, 1));
		assertEquals(cut, spiegelung);
		assertEquals(cut.hashCode(), spiegelung.hashCode());
	}
	
	@Test
	void negativBeispielMitZielfeld() {
		cut = new Schulhof(4, 3, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 11, 12
		}, new Feld(1, 1));
		Schulhof spiegelung = new Schulhof(4, 3, new int[] {
			4, 3, 2, 1,
			8, 7, 6, 5,
			12, 11, 10, 9
		}, new Feld(1, 1));
		assertNotEquals(cut, spiegelung);
		assertNotEquals(cut.hashCode(), spiegelung.hashCode());
	}
}
