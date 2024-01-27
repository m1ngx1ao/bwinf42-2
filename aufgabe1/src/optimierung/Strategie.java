package optimierung;

public interface Strategie {
	/**
	 * @return Eine hoehere Prioritaet bedeutet, dass Nachfolgeknoten bevorzugt
	 * werden sollen. Ein Knoten mit Prioritaet 5 soll also vor einem Knoten
	 * mit Prioritaet 4 bearbeitet.
	 */
	public int berechnePrioritaet(Knoten k);
}
