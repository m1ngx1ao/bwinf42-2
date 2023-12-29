package lauf;

import java.io.IOException;

import optimierung.*;

public class Gierigsuche extends Lauf {
	public static void main(String[] args) throws IOException {
		Optimierer o = new GierigOptimierer(5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				return k.holeSchulhof().holeMaxLaub();
			}
		});
		o.setzteBudgetBlaseOp(500000);

		o.tue();

		Lauf.outputErgebnis(o, Gierigsuche.class.getSimpleName());
	}
}
