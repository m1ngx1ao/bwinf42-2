package modell;

public class Schulhof {
	private int[][] felder;
	private int breite;
	private int hoehe;
	private Feld zielfeld;

	// kalkulierte Attribute
	private int maxLaub;
	private int maxFeldX;
	private int maxFeldY;
	private String repraesentant;

	public Schulhof(int breite, int hoehe, Feld zielfeld) {
		this.zielfeld = zielfeld;
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
	public Schulhof(int breite, int hoehe, int[] felderListe, Feld zielfeld) {
		this.zielfeld = zielfeld;
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
	Schulhof(int[][] felder, Feld zielfeld) {
		this.zielfeld = zielfeld;
		this.felder = felder;
		this.breite = felder[0].length;
		this.hoehe = felder.length;
		berechneAttribute();
	}

	// GETTER

	public Feld holeZielfeld() {
		return zielfeld;
	}

	public int holeBreite() {
		return breite;
	}

	public int holeHoehe() {
		return hoehe;
	}

	public int holeLaub(int x, int y) {
		return felder[y][x];
	}

	public int holeLaub(Feld f) {
		return felder[f.holeY()][f.holeX()];
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
		int zfx = -1;
		int zfy = -1;
		if (zielfeld != null) {
			zfx = zielfeld.holeX();
			zfy = zielfeld.holeY();
		}
		for (int y = 0; y < this.holeHoehe(); y++) {
			String linie = "|";
			for (int x = 0; x < this.holeBreite(); x++) {
				String laubStr = Integer.toString(holeLaub(x, y));
				linie += " ".repeat(4 - laubStr.length()) + laubStr;
				linie += (y == zfy && x <= zfx && x >= zfx - 1) ? "‖" : "|";
			}
			ergebnis += "\n" + linie + "\n" + bindestriche;
		}
		return ergebnis;
	}

	/**
	 * @return Muss fuer aequivalente Schulhoefe dasselbe Ergebnis liefern.
	 * Das ist dann der Fall, wenn die Repraesentanten gleich sind. Das beruecksichtigt
	 * auch das Zielfeld, wenn vorhanden.
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
		if (zielfeld != null) {
			maxFeldX = zielfeld.holeX();
			maxFeldY = zielfeld.holeY();
			maxLaub = holeLaub(maxFeldX, maxFeldY);
			return;
		}
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
	 * 
	 * Wenn ein Zielfeld vorgegeben ist, wird es auch entsprechend gespiegelt und
	 * muss nach der Normalisierung gleich sein, damit Schulhoefe aequivalent sind.
	 */
	private void berechneRepraesentant() {
		String besterKandidat = "";
		// diag/horiz/vert sind wie boolean Variablen
		// -> Spiegelungsachse ist aktiv, wenn sie 1 sind
		for (int diag = 0; diag < ((holeBreite() == holeHoehe()) ? 2 : 1); diag++) {
			for (int horiz = 0; horiz < 2; horiz++) {
				for (int vert = 0; vert < 2; vert++) {
					String kandidat;
					if (zielfeld == null) {
						kandidat = "";
					} else {
						Feld zielfeldGespiegelt = spiegele(false, zielfeld.holeX(), zielfeld.holeY(), diag, horiz, vert);
						kandidat = zielfeldGespiegelt + "@";
					}
					// Aufbau des Kandidaten Zeile fuer Zeile
					for (int y = 0; y < holeHoehe(); y++) {
						for (int x = 0; x < holeBreite(); x++) {
							// x/y aus Sicht des Kandidaten, Transformation zu this Feldern notwendig
							// => umgekehrte Spiegelungsreihenfolge
							Feld gespiegelt = spiegele(true, x, y, diag, horiz, vert);
							if (x + y > 0) {
								// nicht erstes Feld
								kandidat += ",";
							}
							kandidat += holeLaub(gespiegelt);
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
		repraesentant = besterKandidat + "@" + holeBreite() + "," + holeHoehe();
	}

	/**
	 * Benoetigt fuer die Repraesentantenberechnung.
	 * 
	 * @param istUmgekehrt bedeutet, dass die Reihenfolge umgedreht ist. Also ist
	 * spiegele(true, spiegele(false, feld)) dasselbe wie feld (vereinfacht dargestellt).
	 * 
	 * Ein Wert von "1" fuer diag / horiz / vert bedeutet, dass die Spiegelung
	 * in dieser Achse aktiv ist. Sonst ist der Wert "0".
	 */
	private Feld spiegele(boolean istUmgekehrt, int x, int y, int diag, int horiz, int vert) {
		if (!istUmgekehrt) {
			if (vert == 1) {
				y = holeHoehe() - 1 - y;
			}
			if (horiz == 1) {
				x = holeBreite() - 1 - x;
			}
		}
		if (diag == 1) {
			int t = x;
			x = y;
			y = t;
		}
		if (istUmgekehrt) {
			if (horiz == 1) {
				x = holeBreite() - 1 - x;
			}
			if (vert == 1) {
				y = holeHoehe() - 1 - y;
			}
		}
		return new Feld(x, y);
	}
}