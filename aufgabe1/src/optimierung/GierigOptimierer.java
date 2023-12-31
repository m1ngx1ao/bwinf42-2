package optimierung;

import java.util.PriorityQueue;
import java.util.HashSet;
import java.time.Duration;
import java.time.Instant;

import modell.BlaseOp;
import modell.Schulhof;

public class GierigOptimierer extends Optimierer {
	public GierigOptimierer(int breite, int hoehe, Strategie strategie) {
		super(breite, hoehe, strategie);
	}

	@Override
	public void tue() {
		zahlBlaseOps = 0;
		gesehen = new HashSet<String>();
		gesehen.add(start.holeSchulhof().holeRepraesentant());
		PriorityQueue<Knoten> todo = new PriorityQueue<Knoten>();
		besterKnoten = start;
		if (start.holeSchritt() < budgetSchritttiefe) {
			todo.add(start);
		}
		Instant zeitDavor = Instant.now();
		while (!todo.isEmpty() && zahlBlaseOps < budgetBlaseOp) {
			tueNaechsten(todo);
		}
		Instant zeitDanach = Instant.now();
		optimierungsdauer = .001 * Duration.between(zeitDavor, zeitDanach).toMillis();
	}

	private void tueNaechsten(PriorityQueue<Knoten> todo) {
		Knoten aktueller = todo.poll();
		for (BlaseOp blaseOp : blaseOps) {
			Schulhof naechsterSchulhof = blaseOp.tue(aktueller.holeSchulhof());
			zahlBlaseOps++;
			String repraesentant = naechsterSchulhof.holeRepraesentant();
			if (!gesehen.contains(repraesentant)) {
				gesehen.add(repraesentant);
				Knoten naechster = new Knoten(naechsterSchulhof, aktueller, blaseOp);
				maxSchritttiefe = Math.max(maxSchritttiefe, naechster.holeSchritt());
				if (naechsterSchulhof.holeMaxLaub() > besterKnoten.holeSchulhof().holeMaxLaub()) {
					besterKnoten = naechster;
				}
				if (naechster.holeSchritt() < budgetSchritttiefe) {
					naechster.setzePrioritaet(strategie.berechnePrioritaet(naechster));
					todo.add(naechster);
				}
			}
			if (zahlBlaseOps >= budgetBlaseOp) {
				return;
			}
		}
	}
}
