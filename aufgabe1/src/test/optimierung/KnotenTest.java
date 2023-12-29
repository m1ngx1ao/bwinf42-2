package test.optimierung;
import static org.junit.Assert.*;

import org.junit.jupiter.api.Test;

import modell.BlaseOp;
import modell.Schulhof;
import optimierung.Knoten;

public class KnotenTest {
	@Test
	void dreiKnotenKreiertStringZeigtKette() {
		Schulhof anfang = new Schulhof(3, 1);
		Knoten ka = new Knoten(anfang);
		BlaseOp op1 = new BlaseOp(2, 0, -1, 0);
		Schulhof dann = op1.tue(anfang);
		Knoten kd = new Knoten(dann, ka, op1);
		BlaseOp op2 = new BlaseOp(0, 0, 1, 0);
		Schulhof ende = op2.tue(dann);
		Knoten ke = new Knoten(ende, kd, op2);
		assertEquals(2, ke.holeSchritt());
		assertEquals(anfang + "\n" + op1 + "\n" + dann + "\n" + op2 + "\n" + ende, ke.toString());
	}

	@Test
	void knotenHoehererPrioritaetKommtZuerst() {
		Knoten k2 = new Knoten(null);
		k2.setztePrioritaet(2);
		Knoten k5 = new Knoten(null);
		k5.setztePrioritaet(5);
		// Abarbeitungsreihenfolge soll sein: k5 < k2
		assertTrue(k5.compareTo(k2) < 0);
		assertTrue(k2.compareTo(k5) > 0);
	}
}
