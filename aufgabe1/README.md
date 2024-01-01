# Aufgabenstellung

Die Aufgabe wird in zwei Richtungen erweitert:
* Alternativ zum *fest vorgegebenen Zielfeld* wird auch ueberprueft, welche Strategien und Ergebnisse moeglich sind, wenn das Laub auf einem **beliebigem Feld** des Innenhofes (also kein Rand- oder Eckfeld) gesammelt wird.
* Anstatt eine Strategie *heuristisch* vorzudefinieren und damit fest vorzugeben, wird der Baum moeglicher Nachfolgezustaende **iterativ** durchsucht. Die Strategie ergibt sich dann aus der ersten Operation des jeweils besten Unterbaums. Die Aufgabe wird also als **Optimierungsproblem** interpretiert.

# Ansatz

Bei genauerer Betrachtung sieht man, dass die Zustaende nicht als Baum sondern als **Graph** geordnet sind. Das liegt daran, dass zwei verschiedene Zustaende lediglich eine **Spiegelung** voneinander sein koennen. Es reicht dann aus, wenn nur einer der beiden weiter untersucht wird. Dies wird dadurch sichergestellt, dass solch **aequivalente** Zustaende durch einen Lookup ueber ihren **normalisierten Repraesentanten** erkannt werden. Als Folge davon laesst sich je nach Schulhofform (quadratisch vs. rechteckig) und dem Zielfeld (spiegelsymmetrisch fuer alle Spiegelungen) die Zahl der *einzigartigen* Nachfolgezustaende um den Faktor 8 ($2^3$) verringern. Dies aendert auch die Komplexitaetsklasse fuer von $O(f^n)$ zu $O((\frac{f}{8})^n)$, wobei $f$ die Zahl der moeglichen Operationen pro Zustand und $n$ die Zahl der erlaubten Schritte (also Blaseoperationen) sind. In der Implementierung wird von **Knoten** statt *Zustaenden* gesprochen, um die Interpretation als Graphen zu verdeutlichen.

Die Komplexitaetsklasse laesst sich weiter reduzieren, indem auch nur solche Operationen in Betracht gezogen werden, bei denen sich die Laubsituation veraendern kann. Zum Beispiel gibt es auf einem $5*5$ Schulhof an sich $25 * 4 = 100$ Moeglichkeiten zu blasen, da es $4$ Richtungen gibt. Da aber das Blasen gegen den Rand aus der Entferung $0$ oder $1$ zu keiner Aenderung fuehrt (Detaildefinitionen siehe im [Unit Test](src/test/modell/BlaseOpTueTest.java) und in der [Beispielliste](examples.md)), koennen fuer jede Richtung $2*5$ Blaseorte ignoriert werden. Damit gibt es nur $(100-4*2*5)=60$ **potentiell veraendernde** Blaseoperationen, die zu beruecksichtigen sind. Zusammen mit der Aequivalenzbetrachtung ergibt sich also fuer einen $5*5$ Schulhof eine Komplexitaet von $O(7.5^n)$ statt $O(100^n)$.

Dies ist aber natuerlich immer noch viel zu viel, um die moegliche Zugfolgen in die Tiefe untersuchen zu koennen. Entscheidend ist also die **Priorisierung** bei der Durchforstung des Unterbaums, um bei gegebenem Budget die beste Zugfolge moeglichst auch zu finden. Dieser Ansatz aehnelt der **programmatischen Kuenstlichen Intelligenz (KI)** bei Spielen wie Schach (siehe [Deep Blue](https://de.wikipedia.org/wiki/Deep_Blue)). Fuer diese Priorisierung wird eine andersartige Strategie benoetigt. Im Vergleich zur Aufgabenstellen legt sie nur fest, wie erfolgversprechend einzelne Zustaende erscheinen. Ob sie das aber wirklich sind, zeigt nur die Optimierung und Simulation. Es ist also eine Strategie zur Priorisierung der Nachfolgersuche - die tatsaechliche "Zugreihenfolge" ergibt sich aber durch den am Ende gefundenen optimalen Pfad. Im Gegensatz zu Spielen mit mehreren Spielern (wie Schach) beinhaltet diese Zugreihenfolge auch die komplette *Strategie* im Sinne der Aufgabe, da die Reihenfolge durch keine Zuege eines Gegenspielers unterbrochen werden koennen.

Beispiele zu den Konzepten des Ansatzes sind [hier](examples.md).

# Design

Um die Abbildung zu vereinfachen, ist im UML Klassendiagramm Folgendes weggelassen:
* Hole-Methoden: durch die Attributauflistung nicht zwingend erforderlich
* Override von Standard-Methoden (equals, hashCode, toString): im Modell standardmaessig durchgefuehrt aber von der Optimierung nicht benoetigt

``` mermaid
classDiagram
	class Feld {
		-x : int
		-y : int
	}
	class Schulhof {
		-maxLaub : int
		-maxFeldX : int
		-maxFeldY : int
		-breite : int
		-hoehe : int
		-zielfeld : Feld
		-repraesentant : String
		-berechneAttribute()
		+Schulhof(breite : int, hoehe : int, zielfeld : Feld)
		+Schulhof(breite : int, hoehe : int, felderListe : int[], zielfeld : Feld)
		~Schulhof(felder : int[][], zielfeld : Feld)
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
	Feld <.. Schulhof
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
		#outputErgebnis(Optimierer, name : String, zielfeld : Feld)$
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

Jeder der Laeufe ist so parametrisiert, dass er ca. 500.000 Blase-Operationen simuliert und
auswertet. Das dauert ca. 10 Sekunden (Standard Desktop PC). 

Fuer jede Fragestellung fassen zwei Tabellen die Ergebnisse zusammen:
* Die jeweils *beste gefundene Zugreihenfolge* pro Optimierungsansatz und Priorisierungsstrategie. Die Tabelle ist aufsteigend geordnet nach dem besten erzielten Wert.
* Die jeweiligen *Bestwerte* nach einer *Anzahl von Zuegen* pro Optimierungsansatz und Priorisierungsstrategie. Der Bestwert ergibt sich aus dem Laub auf dem Zielfeld wenn vorgegeben oder ansonsten einem beliebigen Innenhof-Feld. Bricht die beste Blasereihenfolge wegen dieser Restriktion der Zahl der simulierten Blase-Operationen schon vor der gegebenen Anzahl der Zuege ab, so ist das mit `---` gekennzeichnet.

## Vorgegebenes Zielfeld (2, 1)

| Lauf/Strategie | Bester Schulhof: Laub auf Innenfeldern | Bester Schulhof: Zahl der benoetigten Blase-Operationen | Einzigartige gesehene Schulhoefe |
| --- | ---: | ---: | ---: |
| Tiefensuche_4 | 400 | 4 | ??? |
| GierigsucheMitBlasekosten_80 | ??? | ??? | ??? |
| GierigsucheMitBlasekosten_40 | ??? | ??? | ??? |
| GierigsucheMitBlasekosten_20 | ??? | ??? | ??? |
| GierigsucheMitBlasekosten_10 | ??? | ??? | ??? |
| Annealingsuche | ??? | ??? | ??? |
| Gierigsuche | ??? | ??? | ??? |
| GierigsucheHeuristikZentrum | ??? | ??? | ??? |

| Lauf/Strategie | 4 | 9 | 13 | 21 | 51 | 703 | 1307 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Tiefensuche_4 | 400 | --- | --- | --- | --- | --- | --- |
| GierigsucheMitBlasekosten_80 | ??? | ??? | --- | --- | --- | --- | --- |
| GierigsucheMitBlasekosten_40 | ??? | ??? | ??? | --- | --- | --- | --- |
| GierigsucheMitBlasekosten_20 | ??? | ??? | ??? | ??? | --- | --- | --- |
| GierigsucheMitBlasekosten_10 | ??? | ??? | ??? | ??? | ??? | --- | --- |
| Annealingsuche | ??? | ??? | ??? | ??? | ??? | ??? | --- |
| Gierigsuche | ??? | ??? | ??? | ??? | ??? | ??? | --- |
| GierigsucheHeuristikZentrum | ??? | ??? | ??? | ??? | ??? | ??? | ??? |

## Beliebiges Zielfeld

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

TBD

Die **Tiefensuche** mit limitierter Tiefe liefert die Basis, was das beste Ergebnis nach einer gewissen (kleinen) Anzahl von Schritte ueberhaupt moeglich ist. Da dabei viele unvorteilhafte Knoten weiter verfolgt werden, fuehrt zu hoher Laufzeit bei schlechtem Ergebnis.

Die **Gierigsuche** verfolgt den jeweils besten Schulhof weiter und fuehrt nur zu einem lokalen Maximum. Da durch weitere Blase-Operationen das Ergebnis immer weiter (aber auch immer weniger) verbessert werden kann, werden lange Ketten von Blase-Operationen untersucht. Dass das Ergebnis nach so vielen Blaseoperationen stark verbessert ist, ist nicht verwunderlich. Auffaellig ist, dass sehr viel weniger einzigartige Schulhoefe im Lauf gesehen werden - nur 92.734 der 500.000 insgesamt moeglichen. Das liegt wohl daran, dass gezielt Permutationen derselben Blaseoperationen ausprobiert werden (und als Duplikate verworfen werden).

Die **Gierigsuche mit Blasekosten** beruecksichtigt die Zahl der benoetigten Blase-Operationen in der Prioritaet, nach der Knoten zur weiteren Verfolgung ausgewaehlt werden. Die Zielfunktion (maximales Laub auf einem der Innenhoffelder) bleibt aber gemaess der Aufgabe diesselbe und beruecksichtigt die Zahl der benoetigten Blase-Operationen nicht. Wie erwartet naehert sich die *Gierigsuche* mit steigendenen *Blasekosten* der Tiefensuche. Besonders interessant ist der Zielkonflikt zwischen Zahl der Schritten und dem erzielten Ergebnis. Waehrend in den ersten Schritten noch knapp 100 Steigerung pro Schritt moeglich sind, faellt dieser Wert auf ca. 10 pro Schritt zwischen dem 10. und 20. Schritt. Am Ende liegt er nur noch bei 3 oder 4. Auch ist bemerkenswert, dass die Laeufe mit geringeren Blasekosten laengerfristig angelegt sind und nach derselben Zahl von Schritten ein vergleichsweise schlechtes Ergebnis haben. Der Schulhof wird also erst "vorbereitet", um danach effizienter zu sein.

Die **Gierigsuche mit Zentrum-Heuristik** geht in eine ganz andere Richtung. In die Prioritaet der gierigen Abarbeitungsreihenfolge geht hier nicht nur der Wert des maximalen Laubs ein. Dazu kommt noch die Summe des Laubes auf allen Innenhoffelder. Diese *Heuristik* basiert auf der Annahme, dass das Laub der Innenhoffelder relativ einfach noch auf das Maximalfeld geblasen werden kann. Das Laub auf ihnen ist also zum guten Teil ein Indikator fuer zukuenftige Erfolge. Das herausragende Ergebnis (ein zur Gierigsuche ueber 50% gesteigerte Zielwert) bestaetigt diese Annahme. Ausserdem ist interessant, dass hier die verfolgten Ketten noch tiefer sind. Durch die staendige Steigerung des Zielwertes kommen Alternativen fuer fruehere Knoten nicht zur Beruecksichtigung.

Als Alternative ist auch die **Annealingsuche** umgesetzt, die das *simulated annealing* implementiert. Mit einer exponentiell fallenden Wahrscheinlichkeit wird zufaellig ein Knoten unabhaengig von seiner Prioritaet auf moegliche Nachfolger untersucht. Diese Wahrscheinlichkeit und ihr Verfall sind so eingestellt, dass im gesamten Lauf ca. 25% die Untersuchungen auf diesem Zufallsprinzip beruhen. Das Ergebnis laesst den Schluss zu, dass diese Randomisierung hier keinen Vorteil bringt. Das laesst sich so interpretieren, dass durch lokale Maxima durch die iterativen Blase-Operationen wenig oder kaum ausgepraegt sind. Durch die Verfolgung zufaelliger Knoten ist das Ergebnis ein bisschen schlechter als beim *gierigen Ansatz*.
