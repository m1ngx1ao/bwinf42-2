package lauf;

import java.io.IOException;

import modell.Feld;
import optimierung.*;

public class Gierigsuche extends Lauf {
	public static void main(String[] args) throws IOException {
		Feld zielfeld = new Feld(2, 1);
		//Feld zielfeld = null;
		Optimierer o = new GierigOptimierer(5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				return k.holeSchulhof().holeMaxLaub();
			}
		}, zielfeld);
		o.setzeBudgetBlaseOp(500000);

		o.tue();

		Lauf.outputErgebnis(o, Gierigsuche.class.getSimpleName(), zielfeld);
	}
}
