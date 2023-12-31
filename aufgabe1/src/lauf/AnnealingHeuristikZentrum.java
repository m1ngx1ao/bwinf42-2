package lauf;

import java.io.IOException;

import modell.Feld;
import optimierung.*;

/**
 * Idee: Laub muss weg vom Schulhofrand gehalten werden, um eine Chance
 * zu haben, es in Folgeschritten zusammenblasen zu koennen.
 * => max-laub hat zwar hohes Gewicht in der Prioritaet,
 *    wird aber von Laub der Innenfelder ergaenzt
 */
public class AnnealingHeuristikZentrum extends Lauf {
	public static void main(String[] args) throws IOException {
		Feld zielfeld = new Feld(2, 1);
		//Feld zielfeld = null;
		Optimierer o = new AnnealingOptimierer(0.4, 5000, 5, 5, new Strategie() {
			@Override
			public int berechnePrioritaet(Knoten k) {
				int res = k.holeSchulhof().holeMaxLaub() * 4;
				for (int x = 1; x < 4; x++) {
					for (int y = 1; y < 4; y++) {
						res += k.holeSchulhof().holeLaub(x, y);
					}
				}
				return res;
			}
		}, zielfeld);
		o.setzeBudgetBlaseOp(500000);

		o.tue();

		Lauf.outputErgebnis(o, AnnealingHeuristikZentrum.class.getSimpleName(), zielfeld);
	}
}
