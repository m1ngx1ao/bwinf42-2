package optimierung;

import modell.BlaseOp;
import modell.Schulhof;

public class Knoten implements Comparable<Knoten>{
	private Schulhof schulhof;
	private Knoten vorgaenger;
	private BlaseOp letzteOp;
	private int schritt;
	private int prioritaet;

	public Knoten(Schulhof schulhof) {
		this.schulhof = schulhof;
		this.vorgaenger = null;
		this.letzteOp = null;
	}

	public Knoten(Schulhof schulhof, Knoten vorgaenger, BlaseOp letzteOp) {
		this.schulhof = schulhof;
		this.vorgaenger = vorgaenger;
		this.letzteOp = letzteOp;
		schritt = vorgaenger.schritt + 1;
	}

	public Schulhof holeSchulhof() {
		return schulhof;
	}

	public int holeSchritt() {
		return schritt;
	}

	public int holePrioritaet() {
		return prioritaet;
	}

	/**
	 * Wird nur einmal gesetzt und nicht bei jedem compareTo
	 * neu berechnet, damit:
	 * (1) Knoten die Strategie nicht kennen muss,
	 * (2) der Vergleich effizient ist (manche Strategien
	 *     koennten aufwaendiger zu berechnen sein)
	 */
	public void setztePrioritaet(int prioritaet) {
		this.prioritaet = prioritaet;
	}

	public String toString() {
		String ergebnis = schulhof.toString();
		if (letzteOp != null) {
			ergebnis = "Op " + schritt + ": " + letzteOp + "\n" + ergebnis;
		}
		if (vorgaenger != null) {
			ergebnis = vorgaenger + "\n" + ergebnis;
		}
		return ergebnis;
	}

	/**
	 * soll K1 vor K2 betrachtet werden, so muss K1 < K2 sein
	 * Das bedeutet fuer ein Knoten KP+ mit hoeherer Prioritaet
	 * im Vergleich zu einem Knoten KP- mit niedriger Prioritaet:
	 * KP+ < KP-
	 * 
	 * Der Vergleich gibt also die gewuenschte zeitliche Abfolge
	 * der Bearbeitung zurueck und nicht den aufsteigende Prioritaeten.
	 */
	@Override
    public int compareTo(Knoten other) {
		return other.holePrioritaet() - this.holePrioritaet();
    }
}