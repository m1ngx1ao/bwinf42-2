package test.modell;
import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import modell.BlaseOp;
import modell.Schulhof;

public class BlaseOpTueTest {
	Schulhof davor;

	@BeforeEach
	void setUp() {
		davor = new Schulhof(5, 3, null);
	}
	
	/**
	 * REGEL: direkt gegen die Wand blasen
	 *   -> verändert nicht die Laub-Situation
	 */
	@Test
	void gegenWandKeineAenderung() {
		Schulhof danach = new BlaseOp(0, 2, -1, 0).tue(davor);
		assertEquals(davor, danach);
		danach = new BlaseOp(3, 2, 0, 1).tue(davor);
		assertEquals(davor, danach);
	}

	/**
	 * REGEL: entlang der Wand (links) blasen
	 *   -> Laub, das auf dem Feld links vorne landen wuerde, landet statt dessen vorne
	 */
	@Test
	void nebenWandNurVorneUndInnen() {
		Schulhof danach = new BlaseOp(1, 0, 1, 0).tue(davor);
		assertNotEquals(davor, danach);
		assertEquals(100, danach.holeLaub(1, 0));
		assertEquals(0, danach.holeLaub(2, 0));
		assertEquals(180, danach.holeLaub(3, 0));
		assertEquals(110, danach.holeLaub(3, 1));
		assertEquals(110, danach.holeLaub(4, 0));
	}

	/**
	 * REGEL: blasen ohne Wand
	 *   -> Resultat ist wie in der Aufgabe vorgegeben
	 */
	@Test
	void ohneWand() {
		Schulhof danach = new BlaseOp(0, 1, 1, 0).tue(davor);
		assertNotEquals(davor, danach);
		assertEquals(100, danach.holeLaub(0, 1));
		assertEquals(0, danach.holeLaub(1, 1));
		assertEquals(170, danach.holeLaub(2, 1));
		assertEquals(110, danach.holeLaub(2, 0));
		assertEquals(110, danach.holeLaub(2, 2));
		assertEquals(110, danach.holeLaub(3, 1));

	}

	/**
	 * REGEL: blasen, mit Wand nach 2 Feldern
	 *   -> die 10% bleiben auf dem "B"
	 */
	@Test
	void vorWandNichtHinten() {
		Schulhof danach = new BlaseOp(1, 0, 0, 1).tue(davor);
		assertNotEquals(davor, danach);
		assertEquals(100, danach.holeLaub(1, 0));
		assertEquals(0, danach.holeLaub(1, 1));
		assertEquals(180, danach.holeLaub(1, 2));
		assertEquals(110, danach.holeLaub(0, 2));
		assertEquals(110, danach.holeLaub(2, 2));
	}

	/**
	 * REGEL: ein Feld von der Wand entfernt
	 *   -> gegen die Wand blasend: es sich verändert nichts
	 */
	@Test
	void vorWandBleibt() {
		Schulhof danach = new BlaseOp(1, 1, 0, -1).tue(davor);
		assertEquals(davor, danach);
	}

}
