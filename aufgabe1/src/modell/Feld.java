package modell;

public class Feld {
	private int x;
	private int y;

	public Feld(int x, int y) {
		this.x = x;
		this.y = y;
	}

	public int holeX() {
		return x;
	}

	public int holeY() {
		return y;
	}

	@Override
	public String toString() {
		return x + "," + y;
	}
}
