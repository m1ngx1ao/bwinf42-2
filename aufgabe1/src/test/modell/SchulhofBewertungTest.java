package test.modell;
import static org.junit.Assert.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import modell.BlaseOp;
import modell.Feld;
import modell.Schulhof;

public class SchulhofBewertungTest {
	Schulhof cut;

	@BeforeEach
	void setUp() {
		cut = new Schulhof(4, 3, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 100, 12
		}, null);
	}
	
	/**
	 * REGEL: Es werden nur die Laubanteile der inneren Felder betrachtet,
	 *   -> da die äußeren nicht vom Traktor abgeholt werden können.
	 */
	@Test
	void maxLaubFeldNurInneres() {
		assertEquals(7, cut.holeMaxLaub());
		assertEquals(2, cut.holeMaxFeldX());
		assertEquals(1, cut.holeMaxFeldY());
	}
	
	/**
	 * Stelle sicher, dass max-Laub/Feld auch fuer Schulhoefe richtig ist,
	 * die aus der Blase-Operation abgeleitet sind.
	 */
	@Test
	void abgeleiteterSchulhofMaxLaubFeldKorrekt() {
		Schulhof act = new BlaseOp(3, 2, -1, 0).tue(cut);
		assertEquals(16, act.holeMaxLaub());
		assertEquals(1, act.holeMaxFeldX());
		assertEquals(1, act.holeMaxFeldY());
	}
	
	/**
	 * Stelle sicher, dass max-Laub nur vom Zielfeld genommen wird,
	 * auch nach Blase-Operation (d.h. der erstellte Schulhoft
	 * uebernimmt das Zielfeld des Vorgaengers).
	 */
	@Test
	void schulhofMitZielfeldMaxLaubFeldKorrekt() {
		cut = new Schulhof(4, 3, new int[] {
			1, 2, 3, 4,
			5, 6, 7, 8,
			9, 10, 100, 12
		}, new Feld(2, 1));
		Schulhof act = new BlaseOp(3, 2, -1, 0).tue(cut);
		assertEquals(7, act.holeMaxLaub());
		assertEquals(2, act.holeMaxFeldX());
		assertEquals(1, act.holeMaxFeldY());
	}
}