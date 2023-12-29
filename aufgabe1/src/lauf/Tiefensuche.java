package lauf;

import java.io.IOException;

import optimierung.*;

public class Tiefensuche extends Lauf {
	private static int BUDGET_SCHRITTTIEFE = 5;

	public static void main(String[] args) throws IOException {
		Optimierer o = new GierigOptimierer(5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				return k.holeSchritt();
			}
		});
		o.setzteBudgetSchritttiefe(BUDGET_SCHRITTTIEFE);

		o.tue();

		Lauf.outputErgebnis(o, Tiefensuche.class.getSimpleName() + "_" + BUDGET_SCHRITTTIEFE);
	}
}
