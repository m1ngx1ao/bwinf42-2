package lauf;

import java.io.IOException;

import optimierung.*;

public class Annealingsuche extends Lauf {
	public static void main(String[] args) throws IOException {
		Optimierer o = new AnnealingOptimierer(0.4, 5000, 5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				return k.holeSchulhof().holeMaxLaub();
			}
		});
		o.setzteBudgetBlaseOp(500000);

		o.tue();

		Lauf.outputErgebnis(o, Annealingsuche.class.getSimpleName());
	}
}
