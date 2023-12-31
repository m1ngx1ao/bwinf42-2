package optimierung;

import java.util.PriorityQueue;
import java.util.Set;
import java.util.HashSet;
import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.ArrayList;

import modell.BlaseOp;
import modell.Schulhof;

/**
 * Die "Temperatur" ist die Wahrscheinlichkeit, dass nicht nach Prioritaet
 * vorgegangen wird, um weitere Knoten zu untersuchen.
 * 
 * Um direkten Indexzugriff auf Knoten der todo-Liste zu erhalten, werden
 * zwei Listen parallel gehalten (Heap fuer Prioritaet und ArrayList fuer Indexzugriff).
 * Ausserdem gibt es einen Lookup fuer schon bearbeitete Knoten, um sie
 * nicht aus der jeweilig anderen Liste loeschen zu muessen (wuerde O(n) kosten).
 */
public class AnnealingOptimierer extends Optimierer {
	private double zufallFaktor;
	private double zufallProb;

	private int zahlBearbeitungZufall;
	private int zahlBearbeitungPrio;

	/**
	 * @param zufallProbAnfang anfaengliche Wahrscheinlichkeit, dass naechster zu bearbeitende
	 * Knoten zufaellig gewaehlt wird
	 * @param zufallHalbiertNach nach so vielen Bearbeitungen von Knoten ist die
	 * Wahrscheinlichkeit, dass naechster zu bearbeitender Knoten zufaellig gewaehlt wird,
	 * nur noch halb so gross
	 */
	public AnnealingOptimierer(double zufallProbAnfang, int zufallHalbiertNach,
			int breite, int hoehe, Strategie strategie) {
		super(breite, hoehe, strategie);
		this.zufallProb = zufallProbAnfang;
		this.zufallFaktor = Math.pow(2, (-1.0 / zufallHalbiertNach));
	}

	public int holeBearbeitungenZufall() {
		return zahlBearbeitungZufall;
	}

    public int holeBearbeitungenPrio() {
        return zahlBearbeitungPrio;
    }

	public void tue() {
		zahlBlaseOps = 0;
		zahlBearbeitungZufall = 0;
		zahlBearbeitungPrio = 0;
		gesehen = new HashSet<String>();
		gesehen.add(initial.holeSchulhof().holeRepraesentant());
		PriorityQueue<Knoten> prioTodo = new PriorityQueue<Knoten>();
		List<Knoten> zufallTodo = new ArrayList<Knoten>();
		// nur zur Ueberpruefung auf identische Knoten
		// => kein equals/hashCode Override fuer Knoten notwendig
		Set<Knoten> bearbeiteteKnoten = new HashSet<Knoten>();

		besterKnoten = initial;
		if (initial.holeSchritt() < budgetSchritttiefe) {
			prioTodo.add(initial);
			zufallTodo.add(initial);
		}
		Instant zeitDavor = Instant.now();

		while (!prioTodo.isEmpty() && zahlBlaseOps < budgetBlaseOp) {
			tueNaechsten(prioTodo, zufallTodo, bearbeiteteKnoten);
		}
		Instant zeitDanach = Instant.now();
		optimierungsdauer = .001 * Duration.between(zeitDavor, zeitDanach).toMillis();
	}

	private void tueNaechsten(PriorityQueue<Knoten> prioTodo, List<Knoten> zufallTodo,
			Set<Knoten> bearbeiteteKnoten) {
		Knoten aktueller;
		if (Math.random() <= zufallProb) {
			zahlBearbeitungZufall++;
			int indexListe = (int) Math.random() * zufallTodo.size();
			aktueller = zufallTodo.get(indexListe);
			// keine Loesung aus prioTodo, da Kosten O(n) sein wuerden
			// keine Loesung aus prioZufall, da Kosten O(n) sein wuerden (Linksschieben)
		} else {
			zahlBearbeitungPrio++;
			aktueller = prioTodo.poll();
			// keine Loesung aus prioZufall, da Kosten O(n) sein wuerden
		}
		// Als Ausgleich fuer fehlendes Wegloeschen, werden bearbeitete
		// (=nach Nachfolgern durchgesuchte) Knoten gemerkt
		if (bearbeiteteKnoten.contains(aktueller)) {
			return;
		}
		bearbeiteteKnoten.add(aktueller);
		// annealing schreitet nur fuer neuen Knoten voran
		zufallProb *= zufallFaktor;
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
					prioTodo.add(naechster);
					zufallTodo.add(naechster);
				}
			}
			if (zahlBlaseOps >= budgetBlaseOp) {
				return;
			}
		}
	}
}
