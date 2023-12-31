package lauf;

import java.io.FileWriter;
import java.io.IOException;

import optimierung.*;

public abstract class Lauf {
    protected static void outputErgebnis(Optimierer o, String name) throws IOException {
        FileWriter fw = new FileWriter("aufgabe1/logs/" + name + ".log");

		fw.write("Optimierungsdauer: " + String.format("%.3f", o.holeOptimierungsdauer()) + " secs");
		fw.write("\nGesehene einzigartige Schulhoefe: " + o.holeZahlEinzigartigerSchulhoefe());
		fw.write("\nDurchgefuehrte Blaseoperationen: " + o.holeZahlBlaseOp());
		fw.write("\nLaengste Schrittfolge: " + o.holeMaxSchritttiefe());
		if (o instanceof AnnealingOptimierer) {
			AnnealingOptimierer ao = (AnnealingOptimierer) o;
			fw.write("\nZufaellige / prioritaetsbasierte Bearbeitungen: "
				+ ao.holeBearbeitungenZufall() + " / " + ao.holeBearbeitungenPrio());
		}
		fw.write("\n\n" + "=".repeat(50) + "\n\n");

        Knoten bester = o.holeBesterKnoten();
		fw.write("Bester Schulhof");
		fw.write("\n  Maximal-Laub: " + bester.holeSchulhof().holeMaxLaub());
		fw.write("\n  Schritte: " + bester.holeSchritt());
		fw.write("\n\n" + bester.toString());

		fw.flush();
		fw.close();
    }
}
