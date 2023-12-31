package lauf;

import java.io.IOException;

import optimierung.*;

public class GierigsucheMitBlasekosten extends Lauf {
	private static int BLASEKOSTEN = 80;

	public static void main(String[] args) throws IOException {
		Optimierer o = new GierigOptimierer(5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				return k.holeSchulhof().holeMaxLaub() - BLASEKOSTEN * k.holeSchritt();
			}
		});
		o.setzeBudgetBlaseOp(500000);

		o.tue();

		Lauf.outputErgebnis(o, GierigsucheMitBlasekosten.class.getSimpleName() + "_" + BLASEKOSTEN);
	}
}
