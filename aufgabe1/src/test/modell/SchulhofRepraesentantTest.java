package test.modell;
import static org.junit.Assert.assertEquals;

import org.junit.jupiter.api.Test;

import modell.Schulhof;

public class SchulhofRepraesentantTest {
	Schulhof cut;

	@Test
	void dreiDreiDurchgezaehlt() {
		cut = new Schulhof(3, 3, new int[] {
			1, 2, 3,
			4, 5, 6,
			7, 8, 9
		});
		assertEquals("9,8,7,6,5,4,3,2,1@3,3", cut.holeRepraesentant());
	}

	@Test
	void dreiDreiMaxInMitte() {
		cut = new Schulhof(3, 3, new int[] {
			1, 2, 7,
			4, 9, 6,
			3, 8, 5
		});
		assertEquals("7,6,5,2,9,8,1,4,3@3,3", cut.holeRepraesentant());
	}

	@Test
	void dreiZweiDurchgezaehlt() {
		cut = new Schulhof(3, 2, new int[] {
			1, 2, 3,
			4, 5, 6
		});
		assertEquals("6,5,4,3,2,1@3,2", cut.holeRepraesentant());
	}

	@Test
	void dreiZweiMaxInMitte() {
		cut = new Schulhof(3, 2, new int[] {
			1, 6, 3,
			4, 2, 5
		});
		assertEquals("5,2,4,3,6,1@3,2", cut.holeRepraesentant());
	}

}
