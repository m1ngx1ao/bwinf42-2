package test.modell;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

import modell.BlaseOp;

class BlaseOpBasisTest {
	BlaseOp cut;

	@Test
	void bewegungRechts() {
		cut = new BlaseOp(0, 1, 1, 0);
		assertEquals("(0, 1) >", cut.toString());
	}

	@Test
	void bewegungLinks() {
		cut = new BlaseOp(2, 1, -1, 0);
		assertEquals("(2, 1) <", cut.toString());
	}

	@Test
	void bewegungOben() {
		cut = new BlaseOp(4, 1, 0, -1);
		assertEquals("(4, 1) ^", cut.toString());
	}

	@Test
	void bewegungUnten() {
		cut = new BlaseOp(1, 1, 0, 1);
		assertEquals("(1, 1) v", cut.toString());
	}

	@Test
	void equalsHash() {
		cut = new BlaseOp(1, 1, 0, 1);
		BlaseOp selbe = new BlaseOp(1, 1, 0, 1);
		BlaseOp andere = new BlaseOp(1, 1, 0, -1);
		assertEquals(cut, selbe);
		assertEquals(cut.hashCode(), selbe.hashCode());
		assertNotEquals(cut, andere);
		assertNotEquals(cut.hashCode(), andere.hashCode());
	}
}