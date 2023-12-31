package test.modell;
import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import modell.Feld;
import modell.Schulhof;

public class SchulhofQuadratAequivalenzTest {
	Schulhof cut;

	@BeforeEach
	void setUp() {
		cut = new Schulhof(4, 4, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 11, 12,
			13, 14, 15, 16
		}, null);
	}
	
	@Test
	void negativBeispiel() {
		Schulhof keineSpiegelung = new Schulhof(4, 4, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 11, 10, 12,
			13, 14, 15, 16
		}, null);
		assertNotEquals(cut, keineSpiegelung);
		assertNotEquals(cut.hashCode(), keineSpiegelung.hashCode());
	}
	
	@Test
	void vertikal() {
		Schulhof spiegelung = new Schulhof(4, 4, new int[] {
			13, 14, 15, 16,
			9, 10, 11, 12,
			5, 6, 7, 8,
			1, 2, 3, 4
		}, null);
		assertEquals(cut, spiegelung);
		assertEquals(cut.hashCode(), spiegelung.hashCode());
	}
	
	@Test
	void horizontal() {
		Schulhof spiegelung = new Schulhof(4, 4, new int[] {
			4, 3, 2, 1,
			8, 7, 6, 5,
			12, 11, 10, 9,
			16, 15, 14, 13
		}, null);
		assertEquals(cut, spiegelung);
		assertEquals(cut.hashCode(), spiegelung.hashCode());
	}
	
	@Test
	void diagonal() {
		Schulhof spiegelung = new Schulhof(4, 4, new int[] {
			1, 5, 9, 13,
			2, 6, 10, 14,
			3, 7, 11, 15,
			4, 8, 12, 16
		}, null);
		assertEquals(cut, spiegelung);
		assertEquals(cut.hashCode(), spiegelung.hashCode());
	}
	
	@Test
	void alleSpiegelungen() {
		Schulhof spiegelung = new Schulhof(4, 4, new int[] {
			16, 12, 8, 4,
			15, 11, 7, 3,
			14, 10, 6, 2,
			13, 9, 5, 1
		}, null);
		assertEquals(cut, spiegelung);
		assertEquals(cut.hashCode(), spiegelung.hashCode());
	}
	
	@Test
	void diagonalSpiegelungMitZielfeld() {
		cut = new Schulhof(4, 4, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 11, 12,
			13, 14, 15, 16
		}, new Feld(2, 1));
		Schulhof spiegelung = new Schulhof(4, 4, new int[] {
			1, 5, 9, 13,
			2, 6, 10, 14,
			3, 7, 11, 15,
			4, 8, 12, 16
		}, new Feld(1, 2));
		assertEquals(cut, spiegelung);
		assertEquals(cut.hashCode(), spiegelung.hashCode());
	}
	
	@Test
	void negativBeispielMitZielfeld() {
		cut = new Schulhof(4, 4, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 11, 12,
			13, 14, 15, 16
		}, new Feld(2, 1));
		Schulhof spiegelung = new Schulhof(4, 4, new int[] {
			1, 5, 9, 13,
			2, 6, 10, 14,
			3, 7, 11, 15,
			4, 8, 12, 16
		}, new Feld(2, 1));
		assertNotEquals(cut, spiegelung);
		assertNotEquals(cut.hashCode(), spiegelung.hashCode());
	}
}
