package lauf;

import java.io.IOException;

import modell.Feld;
import optimierung.*;

public class GierigsucheMitBlasekosten extends Lauf {
	private static int BLASEKOSTEN = 10;

	public static void main(String[] args) throws IOException {
		Feld zielfeld = new Feld(2, 1);
		//Feld zielfeld = null;
		Optimierer o = new GierigOptimierer(5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				return k.holeSchulhof().holeMaxLaub() - BLASEKOSTEN * k.holeSchritt();
			}
		}, zielfeld);
		o.setzeBudgetBlaseOp(500000);

		o.tue();

		Lauf.outputErgebnis(o, GierigsucheMitBlasekosten.class.getSimpleName() + "_" + BLASEKOSTEN, zielfeld);
	}
}
