# Design
Um die Abbildung zu vereinfachen, ist im UML Klassendiagramm Folgendes weggelassen:
* Hole-Methoden: durch die Attributauflistung nicht zwingend erforderlich
* Override von Standard-Methoden (equals, hashCode, toString): im Modell standardmaessig durchgefuehrt aber von der Optimierung nicht benoetigt

``` mermaid
classDiagram
	class Schulhof {
		-maxLaub : int
		-maxFeldX : int
		-maxFeldY : int
		-breite : int
		-hoehe : int
		-repraesentant : String
		-berechneAttribute()
		+Schulhof(breite : int, hoehe : int)
		+Schulhof(breite : int, hoehe : int, felderListe : int[])
		~Schulhof(felder : int[][])
		+existiertFeld(x : int, y : int) boolean
	}
	class BlaseOp {
		-x : int
		-y : int
		-dx : int
		-dy : int
		+tue(davor : Schulhof) Schulhof
		+holeVeraenderndeOps(breite : int, hoehe : int) List~BlaseOp~$
	}
	class Knoten {
		-schritt : int
		-prioritaet : int
		+setzePrioritaet(int)
	}
	class Optimierer {
		<<Abstract>>
		#optimierungsdauer : double
		#zahlBlaseOps : int
		#maxSchritttiefe : int
		#budgetSchritttiefe : int
		#budgetBlaseOp : int
		#gesehen : Set~String~
		+setzeBudgetBlaseOp(int)
		+setzeBudgetSchritttiefe(int)
		+tue()*
	}
	class GierigOptimierer {
		-tueNaechsten(PriorityQueue~Knoten~)
	}
	class AnnealingOptimierer {
		-zufallFaktor : double
		-zufallProb : double
		-zahlBearbeitungZufall : int
		-zahlBearbeitungPrio : int
		-tueNaechsten(PriorityQueue~Knoten~, List~Knoten~, Set~Knoten~)
	}
	class Strategie {
		<<Interface>>
		+berechnePrioritaet(Knoten) int
	}
	Knoten o-- Schulhof
	Knoten --> "0..1" BlaseOp : letzteOp
	Knoten "0..1" <-- Knoten : vorgaenger
	Optimierer --> Knoten : start
	Optimierer --> Knoten : bester
	Optimierer ..> "*" BlaseOp : fuehrt aus
	GierigOptimierer --|> Optimierer
	AnnealingOptimierer --|> Optimierer
	Optimierer o-- Strategie
	class LaufClass["Lauf"] {
		<<Abstract>>
		#outputErgebnis(Optimierer, name : String)$
	}
	class XyzSuche["XYZ-Suche"] {
		+main(args : String[])$
	}
	class XyzSucheAnonymous["Strategie"] {
		<<anonymous>>
	}
	XyzSuche ..> Optimierer : fuehrt aus
	XyzSuche --|> LaufClass
	XyzSucheAnonymous --* XyzSuche
	XyzSucheAnonymous ..|> Strategie
```

# Ergebnisse

Jeder der unteren Laeufe ist so parametrisiert, dass er ca. 500.000 Blase-Operationen simuliert und
auswertet. Das dauert ca. 10 Sekunden (Standard Desktop PC). Die Tabelle ist aufsteigend nach der dem besten erzielten Wert geordnet.

| Lauf/Strategie | Bester Schulhof: Laub auf Innenfeldern | Bester Schulhof: Zahl der benoetigten Blase-Operationen | Einzigartige gesehene Schulhoefe |
| --- | ---: | ---: | ---: |
| Tiefensuche_4 | 400 | 4 | 284.240 |
| GierigsucheMitBlasekosten_80 | 696 | 9 | 398.373 |
| GierigsucheMitBlasekosten_40 | 701 | 13 | 288.035 |
| GierigsucheMitBlasekosten_20 | 765 | 21 | 296.051 |
| GierigsucheMitBlasekosten_10 | 878 | 51 | 305.924 |
| Annealingsuche | 1.347 | 708 | 142.927 |
| Gierigsuche | 1.395 | 703 | 92.734 |
| GierigsucheHeuristikZentrum | 1.954 | 1.307 | 205.300 |

Fuer jeden der besten Blase-Reihenfolgen ist in der folgenden Tabelle festgehalten, welches der Bestwert (Laub auf einem Innenhof-Feld) nach der gegebenen Anzahl von Blasen-Operationen ist. Wie zuvor bekommt jeder Lauf/Strategie ein Budget von ca. 500.000 Blaseoperationen, um dem Bestwert zu kommen. Bricht die beste Blasereihenfolge wegen dieser Restriktion schon vor dem Wert der Spaltenueberschrift ab, so ist das mit `---` gekennzeichnet.

| Lauf/Strategie | 4 | 9 | 13 | 21 | 51 | 703 | 1307 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Tiefensuche_4 | 400 | --- | --- | --- | --- | --- | --- |
| GierigsucheMitBlasekosten_80 | 365 | 696 | --- | --- | --- | --- | --- |
| GierigsucheMitBlasekosten_40 | 357 | 655 | 701 | --- | --- | --- | --- |
| GierigsucheMitBlasekosten_20 | 357 | 576 | 621 | 765 | --- | --- | --- |
| GierigsucheMitBlasekosten_10 | 290 | 374 | 448 | 525 | 878 | --- | --- |
| Annealingsuche | 261 | 360 | 412 | 427 | 505 | 1.345 | --- |
| Gierigsuche | 261 | 360 | 412 | 427 | 505 | 1.395 | --- |
| GierigsucheHeuristikZentrum | 395 | 481 | 555 | 689 | 851 | 1.771 | 1.954 |

# Interpretation

Die **Tiefensuche** mit limitierter Tiefe liefert die Basis, was das beste Ergebnis nach einer gewissen (kleinen) Anzahl von Schritte ueberhaupt moeglich ist. Da dabei viele unvorteilhafte Knoten weiter verfolgt werden, fuehrt zu hoher Laufzeit bei schlechtem Ergebnis.

Die **Gierigsuche** verfolgt den jeweils besten Schulhof weiter und fuehrt nur zu einem lokalen Maximum. Da durch weitere Blase-Operationen das Ergebnis immer weiter (aber auch immer weniger) verbessert werden kann, werden lange Ketten von Blase-Operationen untersucht. Dass das Ergebnis nach so vielen Blaseoperationen stark verbessert ist, ist nicht verwunderlich. Auffaellig ist, dass sehr viel weniger einzigartige Schulhoefe im Lauf gesehen werden - nur 92.734 der 500.000 insgesamt moeglichen. Das liegt wohl daran, dass gezielt Permutationen derselben Blaseoperationen ausprobiert werden (und als Duplikate verworfen werden).

Die **Gierigsuche mit Blasekosten** beruecksichtigt die Zahl der benoetigten Blase-Operationen in der Prioritaet, nach der Knoten zur weiteren Verfolgung ausgewaehlt werden. Die Zielfunktion (maximales Laub auf einem der Innenhoffelder) bleibt aber gemaess der Aufgabe diesselbe und beruecksichtigt die Zahl der benoetigten Blase-Operationen nicht. Wie erwartet naehert sich die *Gierigsuche* mit steigendenen *Blasekosten* der Tiefensuche. Besonders interessant ist der Zielkonflikt zwischen Zahl der Schritten und dem erzielten Ergebnis. Waehrend in den ersten Schritten noch knapp 100 Steigerung pro Schritt moeglich sind, faellt dieser Wert auf ca. 10 pro Schritt zwischen dem 10. und 20. Schritt. Am Ende liegt er nur noch bei 3 oder 4. Auch ist bemerkenswert, dass die Laeufe mit geringeren Blasekosten laengerfristig angelegt sind und nach derselben Zahl von Schritten ein vergleichsweise schlechtes Ergebnis haben. Der Schulhof wird also erst "vorbereitet", um danach effizienter zu sein.

Die **Gierigsuche mit Zentrum-Heuristik** geht in eine ganz andere Richtung. In die Prioritaet der gierigen Abarbeitungsreihenfolge geht hier nicht nur der Wert des maximalen Laubs ein. Dazu kommt noch die Summe des Laubes auf allen Innenhoffelder. Diese *Heuristik* basiert auf der Annahme, dass das Laub der Innenhoffelder relativ einfach noch auf das Maximalfeld geblasen werden kann. Das Laub auf ihnen ist also zum guten Teil ein Indikator fuer zukuenftige Erfolge. Das herausragende Ergebnis (ein zur Gierigsuche ueber 50% gesteigerte Zielwert) bestaetigt diese Annahme. Ausserdem ist interessant, dass hier die verfolgten Ketten noch tiefer sind. Durch die staendige Steigerung des Zielwertes kommen Alternativen fuer fruehere Knoten nicht zur Beruecksichtigung.

Als Alternative ist auch die **Annealingsuche** umgesetzt, die das *simulated annealing* implementiert. Mit einer exponentiell fallenden Wahrscheinlichkeit wird zufaellig ein Knoten unabhaengig von seiner Prioritaet auf moegliche Nachfolger untersucht. Diese Wahrscheinlichkeit und ihr Verfall sind so eingestellt, dass im gesamten Lauf ca. 25% die Untersuchungen auf diesem Zufallsprinzip beruhen. Das Ergebnis laesst den Schluss zu, dass diese Randomisierung hier keinen Vorteil bringt. Das laesst sich so interpretieren, dass durch lokale Maxima durch die iterativen Blase-Operationen wenig oder kaum ausgepraegt sind. Durch die Verfolgung zufaelliger Knoten ist das Ergebnis ein bisschen schlechter als beim *gierigen Ansatz*.
