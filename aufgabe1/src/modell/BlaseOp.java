package modell;

import java.lang.Math;
import java.util.List;
import java.util.LinkedList;

public class BlaseOp {
	private int x;
	private int y;
	private int dx;
	private int dy;

	/**
	 * public, um direkte Tests (auch ohne die statische Fabrikmethode)
	 * zu ermoeglichen
	 */
	public BlaseOp (int x, int y, int dx, int dy) {
		this.x = x;
		this.y = y;
		this.dx = dx;
		this.dy = dy;
	}

	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}

	public int getDX() {
		return dx;
	}

	public int getDY() {
		return dy;
	}

	@Override
	public int hashCode() {
		return (x + "," + y + "," + dx + "," + dy).hashCode();
	}
	
	@Override
	public boolean equals(Object other) {
		if (!(other instanceof BlaseOp)) {
			return false;
		}
		BlaseOp ob = (BlaseOp) other;
		return ob.x == x && ob.y == y && ob.dx == dx && ob.dy == dy;
	}

	public String toString() {
		String richtung = "";
		if (dx == 1) {
			richtung = ">";
		} else if (dx == -1) {
			richtung = "<";
		} else if (dy == 1) {
			richtung = "v";
		} else if (dy == -1) {
			richtung = "^";
		}
		return "(" + x + ", " + y + ") " + richtung;
	}

	public Schulhof tue(Schulhof davor) {
		int hoehe = davor.holeHoehe();
		int breite = davor.holeBreite();
		int[][] neueFelder = new int[hoehe][breite];
		for (int x = 0; x < breite; x++) {
			for (int y = 0; y < hoehe; y++) {
				neueFelder[y][x] = davor.holeLaub(x, y);
			}
		}
		// A und B beziehen sich auf die Felder wie im Beispiel der Aufgabenstellung
		// L und R sind aus Blasrichtung gesehen die Felder oben und unten
		//	 (bzw. links und rechts) von B
		// C ist das Feld hinter B
		int ax = this.x + dx;
		int ay = this.y + dy;
		if (davor.existiertFeld(this.x, this.y) && davor.existiertFeld(ax, ay)) {
			int bx = ax + dx;
			int by = ay + dy;
			int cx = bx + dx;
			int cy = by + dy;
			if (davor.existiertFeld(cx, cy)) {
				int bNachCLaub = Math.round(neueFelder[by][bx] / 10);
				neueFelder[cy][cx] += bNachCLaub;
				neueFelder[by][bx] -= bNachCLaub;
			}
			
			int lx = bx - Math.abs(dy);
			int ly = by - Math.abs(dx);
			int rx = bx + Math.abs(dy);
			int ry = by + Math.abs(dx);
			
			int aLaubZuVerteilen = neueFelder[ay][ax];
			neueFelder[ay][ax] = 0;
			int seitenLaub = Math.round(aLaubZuVerteilen / 10);
			if (davor.existiertFeld(lx, ly)) {
				neueFelder[ly][lx] += seitenLaub;
				aLaubZuVerteilen -= seitenLaub;
			}
			if (davor.existiertFeld(rx, ry)) {
				neueFelder[ry][rx] += seitenLaub;
				aLaubZuVerteilen -= seitenLaub;
			}
			if (davor.existiertFeld(bx, by)) {
				neueFelder[by][bx] += aLaubZuVerteilen;
				aLaubZuVerteilen = 0;
			}
			if (aLaubZuVerteilen != 0) {
				neueFelder[ay][ax] = aLaubZuVerteilen;
			}
		}
		return new Schulhof(neueFelder, davor.holeZielfeld());
	}

	/**
	 * Eine Blase-Operation ist nur dann potenziell veraendernd, wenn sie
	 * die Chance hat die Laubverteilung zu veraendern.
	 * 
	 * Dafuer ist notwendig, dass die Blase-Operation bei der initialen
	 * Verteilung eine Veraenderung hervorruft. Daher wird die Liste
	 * anhand mehrerer Op-Simulationen erstellt.
	 */
	public static List<BlaseOp> holeVeraenderndeOps(int breite, int hoehe) {
		LinkedList<BlaseOp> ergebnis = new LinkedList<BlaseOp>();
		Schulhof s = new Schulhof(breite, hoehe, null);
		for (int dx = -1; dx <= 1; dx++) {
			for (int dy = -1 + Math.abs(dx); dy <= 1 - Math.abs(dx); dy += 2) {
				for (int y = 0; y < hoehe; y++) {
					for (int x  = 0; x < breite; x++) {
						BlaseOp kandidat = new BlaseOp(x, y, dx, dy);
						if (!s.equals(kandidat.tue(s))) {
							ergebnis.add(kandidat);
						}
					}
				}
			}
		}
		return ergebnis;
	}
}