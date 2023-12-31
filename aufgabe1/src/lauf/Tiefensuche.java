package lauf;

import java.io.IOException;

import modell.Feld;
import optimierung.*;

public class Tiefensuche extends Lauf {
	private static int BUDGET_SCHRITTTIEFE = 5;

	public static void main(String[] args) throws IOException {
		Feld zielfeld = new Feld(2, 1);
		//Feld zielfeld = null;
		Optimierer o = new GierigOptimierer(5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				return k.holeSchritt();
			}
		}, zielfeld);
		o.setzeBudgetSchritttiefe(BUDGET_SCHRITTTIEFE);

		o.tue();

		Lauf.outputErgebnis(o, Tiefensuche.class.getSimpleName() + "_" + BUDGET_SCHRITTTIEFE, zielfeld);
	}
}
