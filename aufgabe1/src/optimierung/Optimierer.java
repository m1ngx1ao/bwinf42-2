package optimierung;

import java.util.LinkedList;
import java.util.List;
import java.util.Set;

import modell.BlaseOp;
import modell.Schulhof;

public abstract class Optimierer {
	protected List<BlaseOp> blaseOps = new LinkedList<BlaseOp>();
	
	protected double optimierungsdauer;
	protected int zahlBlaseOps;
	protected int maxSchritttiefe;
	protected Knoten start;
	protected Knoten besterKnoten;

	protected Strategie strategie;

	protected int budgetSchritttiefe;
	protected int budgetBlaseOp;

	/**
	 * Gesehen haelt Repraesentanten (String) und nicht Schulhof
	 * (mehrere Attribute inkl. Felder), um die Groesse
	 * des sets klein zu halten.
	 * Nur die Repraesentanten untereinander nicht aequivalenter Schulhoefe
	 * werde hier abgelegt. Das reicht aus und ist sogar wuenschenswert,
	 * da aequivalente Schulhoefe nur eine blosse Spiegelung sind und nicht
	 * weiter betrachtet werden muessen.
	 */
	protected Set<String> gesehen;
	
	Optimierer(int breite, int hoehe, Strategie strategie) {
		start = new Knoten(new Schulhof(breite, hoehe));
		blaseOps = BlaseOp.holeVeraenderndeOps(breite, hoehe);
		this.strategie = strategie;
		// optionale Beschraenkungen koennen spaeter per setze-Methode
		// angegeben werden. Per default, hier keine Beschraenkung (also "unendlich")
		budgetBlaseOp = Integer.MAX_VALUE;
		budgetSchritttiefe = Integer.MAX_VALUE;
	}

	public Knoten holeBesterKnoten() {
		return besterKnoten;
	}
	
	public double holeOptimierungsdauer() {
		return optimierungsdauer;
	}
	
	/**
	 * 
	 * @return Zahl gesehener einzigartiger Schulhoefe. Einzigartig
	 * bedeutet, dass der Schulhof nicht aequivalent zu anderen ist.
	 */
	public int holeZahlEinzigartigerSchulhoefe() {
		return gesehen.size();
	}

	public int holeZahlBlaseOp() {
		return zahlBlaseOps;
	}

    public int holeMaxSchritttiefe() {
        return maxSchritttiefe;
    }

    public void setzeBudgetSchritttiefe(int tiefe) {
		this.budgetSchritttiefe = tiefe;
    }

	public void setzeBudgetBlaseOp(int blaseop) {
		this.budgetBlaseOp = blaseop;
	}

	// DURCHFUEHRUNG

	public abstract void tue();
}
