package modell;

public class Schulhof {
	private int[][] felder;
	private int breite;
	private int hoehe;

	// kalkulierte Attribute
	private int maxLaub;
	private int maxFeldX;
	private int maxFeldY;
	private String repraesentant;

	public Schulhof(int breite, int hoehe) {
		this.breite = breite;
		this.hoehe = hoehe;
		felder = new int[hoehe][breite];
		for (int x = 0; x < breite; x++) {
			for (int y = 0; y < hoehe; y++) {
				felder[y][x] = 100;
			}
		}
		berechneAttribute();
	}
	
	/**
	 * @param felder Matrix wird fuer eigenes felder-Attribut cloned,
	 *   damit keine Aenderungen am Schulhof von aussen moeglich sind
	 */
	public Schulhof(int breite, int hoehe, int[] felderListe) {
		this.breite = breite;
		this.hoehe = hoehe;
		felder = new int[hoehe][breite];
		for (int y = 0; y < hoehe; y++) {
			for (int x = 0; x < breite; x++) {
				felder[y][x] = felderListe[y * breite + x];
			}
		}
		berechneAttribute();
	}

	/**
	 * @param felder Matrix wird direkt uebernommen.
	 *   Wegen package visibility ist sichergestellt, dass kein Externer die
	 *   so konstruieren und danach die Felder aendern kann.
	 */
	Schulhof(int[][] felder) {
		this.felder = felder;
		this.breite = felder[0].length;
		this.hoehe = felder.length;
		berechneAttribute();
	}

	// GETTER

	public int holeBreite() {
		return breite;
	}
	
	public int holeHoehe() {
		return hoehe;
	}

	public int holeLaub(int x, int y) {
		return felder[y][x];
	}

	public int holeMaxLaub() {
		return maxLaub;
	}

	public int holeMaxFeldY() {
		return maxFeldY;
	}

	public int holeMaxFeldX() {
		return maxFeldX;
	}

	public String holeRepraesentant() {
		return repraesentant;
	}

	// OVERRIDES

	@Override
	public String toString() {
		String bindestriche = "-----".repeat(this.holeBreite()) + "-";
		String ergebnis = bindestriche;
		for (int y = 0; y < this.holeHoehe(); y++) {
			String linie = "|";
			for (int x = 0; x < this.holeBreite(); x++) {
				String laubStr = Integer.toString(holeLaub(x, y));
				linie += " ".repeat(4 - laubStr.length()) + laubStr + "|";
			}
			ergebnis += "\n" + linie + "\n" + bindestriche;
		}
		return ergebnis;
	}

	/**
	 * @return Muss fuer aequivalente Schulhoefe dasselbe Ergebnis liefern.
	 * Das ist dann der Fall, wenn die Repraesentanten gleich sind.
	 */
	@Override
	public int hashCode() {
		return repraesentant.hashCode();
	}
	
	/**
	 * @return Wahr, wenn other aequivalent ist, d.h.
	 * dieselben Dimensionen und dasselbe Laubmuster hat
	 * (oder das fuer Spiegelungen (horizontal, vertikal, diagonal) zutrifft).
	 * Das ist genau dann der Fall, wenn die Repraesentanten gleich sind.
	 */
	@Override
	public boolean equals(Object other) {
		if (!(other instanceof Schulhof)) {
			return false;
		}
		return repraesentant.equals(((Schulhof) other).repraesentant);
	}

	// WEITERE

	public boolean existiertFeld(int x, int y) {
		return x >= 0 && x < holeBreite() && y >= 0 && y < holeHoehe();
	}

	// GIERIGE ATTRIBUTBERECHNUNG (zwecks Effizienz)

	/**
	 * Immer am Ende des Konstruktors aufgerufen. Berechnet alle
	 * abhaengigen Attribute, um spaetere hole-Aufrufe effizient beantworten
	 * zu koennen.
	 */
	private void berechneAttribute() {
		berechneMaxLaubFeld();
		berechneRepraesentant();
	}

	private void berechneMaxLaubFeld() {
		maxFeldX = -1;
		maxFeldY = -1;
		maxLaub = -1;
		for (int x = 1; x < holeBreite() - 1; x++) {
			for (int y = 1; y < holeHoehe() - 1; y++) {
				int laub = felder[y][x];
				if (laub > maxLaub) {
					maxLaub = laub;
					maxFeldX = x;
					maxFeldY = y;
				}
			}
		}
	}

	/**
	 * Alle Schulhoefe mit derselben Normalisierung werden aequivalent genannt (also
	 * sie ergeben sich aus einer Serie von Spiegelungen).
	 * 
	 * Normalisierung bedeutet, einen Repraesentanten des Schulhofes zu bekommen,
	 * der sich, auch wenn der Schulhof gespiegelt wird, genau gleich bleiben wuerde.
	 */
	private void berechneRepraesentant() {
		String besterKandidat = "";
		// diag/horiz/vert sind wie boolean Variablen
		// -> Spiegelungsachse ist aktiv, wenn sie 1 sind
		for (int diag = 0; diag < ((holeBreite() == holeHoehe()) ? 2 : 1); diag++) {
			for (int horiz = 0; horiz < 2; horiz++) {
				for (int vert = 0; vert < 2; vert++) {
					String kandidat = "";
					// Aufbau des Kandidaten Zeile fuer Zeile
					for (int y = 0; y < holeHoehe(); y++) {
						for (int x = 0; x < holeBreite(); x++) {
							// x/y aus Sicht des Kandidaten, Transformation zu this Feldern notwendig
							int sx = x;
							int sy = y;
							if (diag == 1) {
								int t = sx;
								sx = sy;
								sy = t;
							}
							if (horiz == 1) {
								sx = holeBreite() - 1 - sx;
							}
							if (vert == 1) {
								sy = holeHoehe() - 1 - sy;
							}
							kandidat += "," + felder[sy][sx];
						}
					}
					// der lexikografisch groesste Kandidat wird genommen
					// eine andere Wahl waere auch moeglich - entscheidend ist:
					// jeden aequivalenten Schulhof bekommt dieselbe Normalisierung
					if (kandidat.compareTo(besterKandidat) > 0) {
						besterKandidat = kandidat;
					}
				}
			}
		}
		// Komma entfernen...
		repraesentant = besterKandidat.substring(1) + "@" + holeBreite() + "," + holeHoehe();
	}
}