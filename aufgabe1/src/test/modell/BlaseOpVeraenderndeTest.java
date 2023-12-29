package test.modell;
import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import org.junit.jupiter.api.Test;

import modell.BlaseOp;
import modell.Schulhof;

public class BlaseOpVeraenderndeTest {
	Schulhof davor;

	@Test
	void fuenfMalFuenf60() {
		List<BlaseOp> res = BlaseOp.holeVeraenderndeOps(5, 5);
		assertEquals(60, res.size());
		assertFalse(res.contains(new BlaseOp(1, 2, -1, 0)));
		assertTrue(res.contains(new BlaseOp(1, 2, 1, 0)));
	}

	@Test
	void dreiMalFuenf80() {
		List<BlaseOp> res = BlaseOp.holeVeraenderndeOps(3, 5);
		assertEquals(28, res.size());
		assertFalse(res.contains(new BlaseOp(1, 2, -1, 0)));
	}
}
