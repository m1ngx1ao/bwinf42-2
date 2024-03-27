# Aufgabenstellung

In der Aufgabe wird nach einem Besiedlungsplan gesucht, der eine maximale Anzahl von Ortschaften im Gebiet platziert unter Berücksichtigung der Mindestabstände. Dazu soll es **genau ein** Gesundheitszentrum geben, da *"... genügend Geld zur Verfügung \[stehe\], um ein Gesundheitszentrum zu bauen"*.

In der Realität werden hingegen bei *Investitionsentscheidungen* der **Nutzen** und die **Kosten** gegenübergestellt. In diesem Fall ist also die Frage, wie viele weitere Ortschaften in den Besiedlungsplan korrekt aufgenommen werden können, wenn ein Gesundheitszentrum **zusätzlich** gebaut wird. Diese Frage muss für jede (sinnvolle) Zahl von Gesundheitszentren beantwortet werden. Darauf basierend kann der Planer den optimalen Besiedlungsplan wählen und umsetzen.

## Beispiel zur Aufgabenstellung

Für *ein gegebenes Gebiet* und *den Mindestabständen zwischen Ortschaften* werden folgende optimale Pläne *abhängig von der Zahl der Gesundheitszentren* gefunden:

| # Gesundheitszentren | # Ortschaften |
| --: | --: |
| 0 | 43 |
| 1 | 107 |
| 2 | 125 |
| 3 | 127 |

Das erste Gesundheitszentrum lohnt sich also, wenn seine Kosten den Nutzen $(107-43)=64$ zusätzlicher Ortschaften unterschreitet. Beim zweiten müssten die Kosten unter dem Nutzen $(125-107)=18$ zusätzlicher Ortschaften liegen. Und das dritte Gesundheitszentrum erlaubt nur $(127-125)=2$ weitere Ortschaften, seine Kosten übersteigen hier also wohl den Nutzen dieser beiden Ortschaften.

Während die ursprüngliche Aufgabestellung also nur eine Zeile der Tabelle fordert, wird die Aufgabenstellung so erweitert, dass nach der gesamten Tabelle gesucht wird.

# Ansatz

Der Besiedlungsplan wird *schrittweise* um *je eine Ortschaft* erweitert. Bei jedem Schritt werden die *Abstandsbedingungen* überprüft und der Plan so *optimiert*, dass diese Bedingungen alle erfüllt sind. Wenn dies auch nach mehrmaligen Versuchen nicht erfolgreich ist, wird *ein Gesundheitszentrum* hinzugefügt.

Die Kernpunkte des Ansatzes sind also wie folgt:
* **Optimierer**: Für einen gegebenen Plan werden Ortschaften und Zentren so lange innerhalb des Gebiets verschoben, bis alle Abstandsbedingungen erfüllt sind. Dazu werden in jeder Iteration Plankandidaten durch Punktverschiebung generiert. Diese Kandidaten werden anhand ihres *Loss* beurteilt, der sich aus der Summe fehlender Abstände zwischen Punktpaaren berechnet. Bei der gierigen Optimierung wird dann der Kandidat mit dem geringsten *Loss* für die nächste Iteration ausgewählt. Liegt der *Loss* bei Null, ist eine *zulässige* Lösung gefunden und die Optimierung beendet. Ansonsten wird die Optimierung mit einer *unzulässigen* Lösung *abgebrochen*, wenn die Zahl der Iterationen einen Schwellwert überschreitet oder seit zu vielen Iteration keine Verminderung des Loss eingetreten ist.
* **Lauf**: Startend von einem *leeren* Gebiet wird eine Ortschaft nach der nächsten *zufällig innerhalb* des Gebiets platziert. Wird der Plan dadurch *unzulässig*, werden die Planpunkte durch die *Optimierung* so *angepasst*, dass der Plan *zulässig* wird. Ist dies nicht möglich, wurde die Ortschaft eventuell an einer Engstelle platziert. Als eine Art *Backtracking* werden daher weitere *zufällige Platzierungen* für die neue Ortschaft ausprobiert (Lauf-Iteration). Scheitern diese Versuche, ist davon auszugehen, dass das Gebiet keine weitere Ortschaft aufnehmen kann. Daher wird ein *Gesundheitszentrum hinzugefügt* und mit der zufälligen Platzierung der neuen Ortschaft erneut begonnen. Der Lauf endet, wenn bereits so viele Zentren auf dem Plan sind, dass das gesamte Gebiet von ihnen praktisch abgedeckt werden könnte (in den Beispieldaten bei ca. drei Zentren der Fall).

Es ergibt sich die folgende *Ablauflogik*:

``` mermaid
graph TD
	subgraph Lauf
		LaufIter[Lauf-Iteration LI: \n Füge Ortschaft dem letzten zulässigen Plan hinzu]
		LaufIterLoss{Loss = 0?}
		LaufInBudget{#LI < Budget?}
		LaufZentrumDazu[Füge Zentrum dem letzten \n zulässigen Plan hinzu]
		LaufZentrumInBudget{#Zentren \n < Budget?}
	end
	subgraph Optimierer
		OptIter[Optimierer-Iteration OI: \n Generiere Planvarianten \n und wähle die beste aus]
		OptIterLoss{Loss = 0?}
		OptInBudget{#OI < Budget?}
	end
	S[Starte mit leerem Plan] --> LaufIter
	LaufIter --> LaufIterLoss
	LaufIterLoss -- ja --> LaufIter
	LaufIterLoss -- nein --> OptIter
	OptIter --> OptIterLoss
	OptIterLoss -- ja --> LaufIter
	OptIterLoss -- nein --> OptInBudget
	OptInBudget -- ja --> OptIter
	OptInBudget -- nein --> LaufInBudget
	LaufInBudget -- ja --> LaufIter
	LaufInBudget -- nein --> LaufZentrumInBudget
	LaufZentrumInBudget -- ja --> LaufZentrumDazu
	LaufZentrumDazu --> LaufIter
	LaufZentrumInBudget -- nein --> E[Ende]
```

Für die Komplexitätsbetrachtung sind zwei Aspekte von Interesse. Hierfür sei die Zahl der *Ortschaften* $n$, der *Gesundheitszentren* $z$ und diejenige der *Eckpunkte des Gebietspolygons* $g$:
* **Loss-Berechnung**: Vorab ist in $O(n\cdot z)$ zu überprüfen, welche Orte von Zentren geschützt sind. Darauf basierend lässt sich für Ortspaare deren Abstand berechnen und auf Zulässigkeit überprüfen. Wird dies für *alle* Ortspaare gemacht, würde dies $O(n^2)$ an Aufwand bedeuten. Um das zu vermeiden, werden die Ortschaften in *Planquadrate* aufgeteilt, deren Seitenlänge der *strengsten* Abstandsregel entspricht (in der Aufgabenstellung also *20 km*). Dann müssen nur für Ortspaare *benachbarter* Planquadrate die Abstände berechnet und überprüft werden (auch diagonale Nachbarschaft berücksichtigt). Da sowohl die Zahl der Ortschaften pro Planquadrat als auch die Zahl benachbarter Planquadrate *konstant* ist, fällt nur der *assoziative Zugriff* auf Planquadrate mit $O(\log n)$ bei der Komplexitätsbetrachtung in Gewicht. Dies führt zum Aufwand von $O(n \log n)$ für die Ortspaare. Zusammen ergibt das $O(n\cdot (z+\log n))$.
* **Gebiet-Überprüfung**: Mit dem *Punkt-in-Polygon* Algorithmus erfordert die Überprüfung eines Punkts $Θ(g)$. Jeder Punkt wird so lange von seinem Ausgangspunkt verschoben, bis er innerhalb des Gebiets liegt. Da hierbei die Punktabstände nicht berücksichtigt werden, gibt es abhängig von der Gebietsform einen konstanten Faktor, der sich aus der Wahrscheinlichkeit vergeblicher Versuche ergibt. Dieser ist für die Komplexitätsklasse unerheblich. Da nicht immer alle Punkte bewegt werden und für unbewegte Punkte die Gebiet-Überprüfung schon erfolgt ist, liegt der Aufwand für einen Plankandidaten somit bei $O(g\cdot (n+z))$.

Daraus ergibt sich folgende Komplexität für die Elemente der Ablauflogik:
* *Optimierer-Iteration:* Die Zahl der Kandidaten ist durch Konstanten festgelegt. Damit ergibt sich die Komplexität direkt aus der Kombination der *Loss-Berechnung* und der *Gebiet-Überprüfung*, also: $$O\bigl(n\log n + n\cdot (g+z)+g\cdot z\bigr)$$
* *Lauf-Iteration:* Auch hier ist durch Konstanten festgelegt, wie viele Iterationen maximal vom Optimierer durchlaufen werden und wie viele Platzierungen der neuen Ortschaft versucht werden dürfen. Die Komplexität ist also dieselbe wie die einer *Optimierer-Iteration*.
* *Gesamter Lauf:* Der Besiedlungsplan durch schrittweiser Hinzunahme von Ortschaften aufgebaut. Wenn $n$ die Ortschaften der abschließenden Lösung darstellt sind also $Θ(n)$ Schritte obiger Komplexität durchzuführen. Dabei ist unerheblich, dass $n$ anfangs kleiner ist, da dies im Schnitt nur einen konstanten Faktor ausmacht. Für die Komplexität des gesamten Laufs gilt also: $$O\bigl(n^2\log n + n^2\cdot (g+z)+n\cdot g\cdot z\bigr)$$

Prinzipiell gibt es auch alternative Lösungsansätze, die hier nicht weiter verfolgt werden. Dies liegt an Folgendem:
* **Analytische** bzw. **konstruierende** Ansätze sind wenig vielversprechend. Dies liegt an der Form der Siedlungsgebiete, die nicht einmal *konvex* sind. Eine Ausnahme ist das quadratische Siedlungsgebiet von *Siedler3*. Aber selbst hier lässt sich nur dann beweisbar optimal konstruieren, wenn kein Gesundheitszentrum verwendet wird.
* Die Verwendung von **Loss-Gradienten** *("Abstoßung")* bei der Punktverschiebung ist schwierig, da dann auch der Verbleib / die Rückkehr in die Gebietsgrenzen *("Anziehung")* mathematisch erfasst werden müsste. Daher wird auf sie verzichtet. Dennoch ist die Optimierung *zielgerichtet*, da der stetige Loss für die Kandidatenauswahl verwendet wird. Insofern bekommt der Optimierer selbst bei unzulässigen Planen ein Hinweis darauf, welcher Kandidat die Punkte am meisten in die richtige Richtung verschoben hat.
* Die vorgestellte Methode zur Planwahl einer Optimierer-Iteration ist *gierig*. Dies würde ein Problem darstellen und potenziell zu *lokalen Optima* führen, wenn Folgepläne anhand der *Gradienten* deterministisch bestimmt würden. Dies aber nicht der Fall ist, da Planpunkte *zufällig* bewegt werden. Daher kann auf zusätzliche Methoden der Planwahl (z.B. *Annealing*) verzichtet werden.

# Design

Um die Abbildung zu vereinfachen, ist im UML Klassendiagramm Folgendes weggelassen:
* Hole-Methoden: durch die Attributauflistung nicht zwingend erforderlich.
* Inhalt des Files "types.py", da dieser nur TPunkt (siehe unten) enthaelt.
* Override von Standard-Methoden (lt, str): im Modell standardmässig durchgeführt
* Konstruktoren: nur aufgelistet, wenn ihre Parameter sich maßgeblich von den Attributen unterscheiden.
* konstante Variablen, wie zum Beispiel im "Plotter" die Farben der gueltigen Ortschaften.

Außerdem wird für den Typ einen Punkt `tuple[float, float]` ein spezifischer Typ `TPunkt` verwendet. Mit Punkt sind alle Modellpunkte gemeint, also Ortschaften, Gesundheitszentren und Polygonecken.
`+/-` vor den Attributen bedeutet, dass das Attribut von außen nicht veränderbar ist, jedoch auf den Inhalt des Attributs durch die Hole-Methoden Zugriff hat.

Die Unterklassen von Beobachter werden in einem separaten Schaubild dargestellt.

``` mermaid
classDiagram
	class Parameter {
		+min_abstand : float
		+sicher_abstand_ab : float
		+schutz_zentrum_bis : float
	}
	class Gebiet {
		+/-linienzug : list~TPunkt~
		+/-eckpunkte : frozenset~TPunkt~
		+/-name : str
		+von_datei(datei_name) Gebiet$
		+ist_drin(TPunkt)
		+zufaelliger_punkt() TPunkt
	}
	class Besiedlungsplan {
		+/-orte : frozenset~TPunkt~
		+/-zentren : frozenset~TPunkt~
		+/-geschuetzte_orte : frozenset~TPunkt~
		+/-zunahe_orte : frozenset~TPunkt~
		+/-ausserhalb_gebiet_orte : frozenset~TPunkt~
		+/-loss : float
		-auswerte_gebiet()
		-auswerte_ort_abstand()
		-berechne_abstand(TPunkt, TPunkt)
		-berechne_ausserhalb_gebiet_orte(orte) set~TPunkt~
		-berechne_geschuetzte_orte(zentren, orte) set~TPunkt~
	}
	Besiedlungsplan "*" --> "1" Parameter
	Besiedlungsplan "*" --> "1" Gebiet

	class GierigOptimierer {
		-bewege_punkt(TPunkt, Besiedlungsplan) TPunkt
		-erstelle_kandidat(Besiedlungsplan, *optionen) Besiedlungsplan
		+tue() tuple~int, Besiedlungsplan~
	}
	GierigOptimierer --> "1" Besiedlungsplan : Start

	class GierigLauf {
		-budget_zentren: int
		+tue()
	}
	GierigLauf "*" --> "1" Parameter
	GierigLauf "*" --> "1" Gebiet
    GierigLauf ..> GierigOptimierer
	GierigLauf ..> Besiedlungsplan

	class Beobachter {
		<<Abstract>>
		+optimierer_start(Besiedlungsplan, strategie: str) *
		+optimierer_iteration(Besiedlungsplan) *
		+optimierer_ende() *
		+lauf_start(Besiedlungsplan, strategie: str) *
		+lauf_loesung(Besiedlungsplan, benoetigte_iter_num) *
		+lauf_ende(self) *
	}
	GierigOptimierer --> "*" Beobachter
	GierigLauf --> "*" Beobachter
	Beobachter ..> Besiedlungsplan
```

Die verschiedenen Unterklassen von Beobachter sind für die Verfolgung und Protokollierung des Laufs und Optimierers zuständig. Sie sind im folgenden Schaubild dargestellt.

``` mermaid
classDiagram
	class Beobachter {
		<<Abstract>>
		+optimierer_start(Besiedlungsplan, strategie: str) *
		+optimierer_iteration(Besiedlungsplan) *
		+optimierer_ende() *
		+lauf_start(Besiedlungsplan, strategie: str) *
		+lauf_loesung(Besiedlungsplan, benoetigte_iter_num) *
		+lauf_ende(self) *
		-garantiere_kein_file(pfad: str)
		-garantiere_leeren_folder(pfad: str)
		-garantiere_folder(Besiedlungsplan, strategie: str, modul: str) str
		#vorbereite_output_file(Besiedlungsplan, strategie: str, modul: str, file_name) str
		#vorbereite_output_folder(Besiedlungsplan, strategie: str, modul: str, folder_name) str
	}
	class Trafo {
		+min_x : float
		+max_x : float
		+min_y : float
		+max_y : float
		+zoom_x : float
		+zoom_y : float
		+rand: float
		-Trafo(punkte: frozenset~TPunkt~, rand: float, breite: float, hoehe: float)
	}
	class Plotter {
		-fenster : tk.Tk
		-canvas : tk.Canvas
        -male(Besiedlungsplan)
        -male_zentren(Trafo, Besiedlungsplan)
        -male_orte(Trafo, Besiedlungsplan)
		-male_gebiet(Trafo, Besiedlungsplan)
		-speichere_canvas_to_file(lauf_name, iter_num)
	}
    Plotter ..|> Beobachter
    Plotter ..> Trafo
	class Logger {
		-iter_num : int
		-f: TextIOWrapper
		-ausgabe(str)
	}
	Logger ..|> Beobachter
	class Stats {
		_iter_num : int
		-f: TextIOWrapper
		-ausgabe(list~str | float | int~, ort: io.TextIOWrapper)
	}
	Stats ..|> Beobachter
```

# Durchführung: Erstellung der Besiedlungspläne

Die fünf vorgegebenen *Siedlungsgebiete* haben sehr reguläre Formen, die sich zur Untersuchung gewisse Aspekte des Ansatzes sehr gut eignen. Was allerdings fehlt, ist ein Siedlungsgebiet, das insofern *realistisch* ist, als dass es die *Unförmigkeiten* von Landesgrenzen oder Küstenverläufen abbildet. Dazu eignet sich das *griechische Festland* mit seinen *zerklüfteten Küsten* und *konkaven Elementen* hervorragend. Außerdem ist zu untersuchen, wie gut der Lösungsansatz mit der Komplexität des Gebiets und der verfügbaren Fläche *skaliert*.

Dafür wurde ein *sechstes* Gebiet erstellt und der Evaluationsreihe hinzugefügt. Seine Koordinaten sind im *korrekten* Maßstab (km) angegeben, womit die Abstandsregeln (10 km, 20 km, 85 km) besser *veranschaulicht* werden und eine viel größere Fläche als in den vorgegebenen Gebieten zu besiedeln ist (Achse von Nord-Süd und West-Ost ist knapp *600 km*). Außerdem besteht sein Polygon aus *165* Eckpunkten, was weitaus mehr als die *4-22* Eckpunkte der vorgegebenen Gebiete ist. Damit lässt sich die *Skalierbarkeit* der Polygon-Algorithmen auf die Probe stellen.

| ![hellas](docs/gebiet-griechenland.png) |
| :--: |
| Zusätzliches Siedlungsgebiet: Griechisches Festland als *165-Eck* im korrekten Maßstab *(km)*, <br> also mit einer Achsenlänge von *fast 600* |

Für jedes Siedlungsgebiet wurde je ein Optimierungslauf auf einem Desktop PC mit dem *AMD FX8330* Prozessor durchgeführt. Dabei wurde Standard-Python im Terminal verwendet und auf Compilierung mit etwa *Cython* oder *PyPy* verzichtet. Die Dauer pro Lauf ist wie folgt:

| Gebiet | Siedler1 | Siedler2 | Siedler3 | Siedler4 | Siedler5 | Griechenland |
| -- | --: | --: | --: | --: | --: | --: |
| Dauer / min | 83 | 62 | 103 | 132 | 68 | 2851 |

# Ergebnisse

## Vorgegebene Siedlungsgebiete

In der Aufgabenstellung wird nach dem Zusammenhang gefragt zwischen der Zahl der verfügbaren Gesundheitszentren und der Anzahl der Ortschaften, die damit zulässig platziert werden können. Dies wird in der folgenden Tabelle und dem Schaubild festgehalten.

| # Gesundheits-<br>zentren | # Ortschaften <br> @ Siedler1 | # Ortschaften <br> @ Siedler2 | # Ortschaften <br> @ Siedler3 | # Ortschaften <br> @ Siedler4 | # Ortschaften <br> @ Siedler5 |
| --: | --: | --: | --: | --: | --: |
| 0 | 39 | 37 | 49 | 49 | 41 |
| 1 | 109 | 81 | 158 | 132 | 128 |
| 2 | 129 | 81 | 162 | 150 | 131 |
| 3 | 132 | 83 | 163 | 152 | 133 |

![ch-orte-pro-zentren](docs/orte-pro-zentren.svg)

Die zugehörigen Plankarten sind im Folgenden abgebildet. Sie sind auf eine *quadratische* Zeichenfläche normalisiert. Die unterschiedlichen *Zoomfaktoren* in x/y-Richtung werden z.B. bei *Siedler4* und *Siedler5* durch die *elliptischen* Schutzgebiete der Gesundheitszentren deutlich. Die Plan-Rohdaten finden sich in `output/siedler*/gierig/lauf/plandaten`.

| Gebiet | *Kein* Zentrum | *Ein* Zentrum | *Zwei* Zentren | *Drei* Zentren |
| -- | -- | -- | -- | -- |
| Siedler1 | ![s1k0](output/siedler1/gierig/lauf/karten/039.png) | ![s1k1](output/siedler1/gierig/lauf/karten/109.png) | ![s1k2](output/siedler1/gierig/lauf/karten/129.png) | ![s1k3](output/siedler1/gierig/lauf/karten/132.png) |
| Siedler2 | ![s2k0](output/siedler2/gierig/lauf/karten/037.png) | ![s2k1](output/siedler2/gierig/lauf/karten/081.png) | | ![s2k3](output/siedler2/gierig/lauf/karten/083.png) |
| Siedler3 | ![s3k0](output/siedler3/gierig/lauf/karten/049.png) | ![s3k1](output/siedler3/gierig/lauf/karten/158.png) | ![s3k2](output/siedler3/gierig/lauf/karten/162.png) | ![s3k3](output/siedler3/gierig/lauf/karten/163.png) |
| Siedler4 | ![s4k0](output/siedler4/gierig/lauf/karten/049.png) | ![s4k1](output/siedler4/gierig/lauf/karten/132.png) | ![s4k2](output/siedler4/gierig/lauf/karten/150.png) | ![s4k3](output/siedler4/gierig/lauf/karten/152.png) |
| Siedler5 | ![s5k0](output/siedler5/gierig/lauf/karten/041.png) | ![s5k1](output/siedler5/gierig/lauf/karten/128.png) | ![s5k1](output/siedler5/gierig/lauf/karten/131.png) | ![s5k2](output/siedler5/gierig/lauf/karten/133.png) |

Aus den Plankarten lassen sich folgende Erkenntnisse gewinnen:
* *Gesundheitszentren* werden im Zuge des Lauf in sinnvolle Positionen verschoben. So ist z.B. für *Siedler5* das erste Gesundheitszentrum *mittig* angelegt, während beim Hinzufügen eines zweiten beide Zentren sich auf beide Seiten *verteilen*. Dies beweist den Kerngedanken des Lösungsansatzes, dass auch ohne *Gradienten* nur basierend auf *Loss* eine **zielgerichtete Optimierung** stattfinden kann. Das gilt auch für bereits platzierte Ortschaften und wird aus den Optimierungsverläufen klarer deutlich. Detailliertere Beispiele aus dem Anhang:
	* *Schleichende Migration*: Das erste Gesundheitszentrum von *Siedler1* fängt am Rand an und bewegt sich dann in Richtung Mitte. Die verkürzte Darstellung des Laufes ist [hier](#siedler-1).
	* *Überwinden von Gebietslücken:* Auch *Lücken* im Gebiet werden erfolgreich übersprungen. Ein Beispiel für *Siedler5* ist [hier](#siedler5-bei-128-130-ortschaften-und-1-2-gesundheitszentren) und für das *griechische Festland* [hier](#griechisches-festland-bei-813-ortschaften-und-8-gesundheitszentren).
* Die *spitzen Ecken* von *Siedler2* und *Siedler4* sind an sich vielversprechende Punkte für das Setzen der Ortschaften. Jedoch ist der hier verfolgte Lösungsansatz **generisch** gehalten. Er besitzt also *keine Sonderlogik*, um solche Ecken zu erkennen und zu berücksichtigen. Als Folge davon nutzen die erstellten Besiedlungspläne den Platz um die spitzen Ecken nicht immer voll aus.
* Die *Zufälligkeit* des Laufs und Optimierers wird z.B. in *Siedler2* deutlich. Dort wären die Besiedlungspläne ab *82* Ortschaften auch für nur *1* Gesundheitszentrum möglich gewesen. Auch bei anderen Plänen ist also davon auszugehen, dass minimal bessere Besiedlungspläne bei erneutem Durchlauf gefunden werden könnten. Dennoch ist das **Optimierungsergebnis** in der Hinsicht **robust**, dass der Zufall nur einen kleinen Einfluss auf die Zahl der erreichten Ortschaften hat ($\pm 2\%$ bei *Siedler2*).

Der Schwierigkeitsgrad der Optimierung steigt mit der Zahl der Ortschaften. Wenn die Optimierung zu schwierig wird, sorgt die Budgetierung des *Laufs* und des *Optimierers* dafür, dass ein Gesundheitszentrum hinzugefügt oder der Lauf beendet wird. Dies wird im folgenden Schaubild veranschaulicht. Als Schwierigkeitsgrad wird hierbei die Zahl der *Optimierer-Iterationen* genommen, die zwischen zwei *zulässigen* Besiedlungsplänen benötigt wurden. Dies berücksichtigt sowohl die Neuplatzierungen der zusätzlichen Ortschaft als auch die nachfolgenden Punktbewegungen des Optimierers. Es werden jeweils die Stammfunktionen gezeigt, da die Verläufe sich sonst oft überschneiden würden. Die *Steigung* der Verläufe zeigt also den *Schwierigkeitsgrad*.

![ch-opiter-pro-orte](docs/opiter-pro-orte.svg)

Wie erwartet steigt der Schwierigkeitsgrad *vor* Hinzunahme des Gesundheitszentrums. *Danach* ist er wieder minimal, außer wenn keine zusätzliche Abdeckung durch das Gesundheitszentrum erzielt werden kann. Außerdem lässt sich erkennen, dass der erhöhte Schwierigkeitsgrad nicht abrupt einsetzt, sondern sich kontinuierlich aufbaut. Dies ergibt sich daraus, dass die Wahrscheinlichkeit, eine zulässige Lösung ohne Hinzunahme eines weiteren Gesundheitszentrums zu finden, stetig abnimmt.

## Zusätzliches Siedlungsgebiet

Auch für das *griechische Festland* als *realitätsnäheres* und *größeres* Siedlungsgebiet sind die Ergebnisse im Folgenden festgehalten.

Die Laufzeit ist um den *Faktor* **21,6** länger als die längste Laufzeit der vorgegebenen Siedlungsgebiete (*2851 min* statt maximal *132 min*). Dies liegt unter dem Faktor, der aufgrund obiger *Komplexitätsbetrachtung* zu erwarten wäre. Im Einzelnen sind die *eingehenden Faktoren*:
* Ortschaften ($n$): Faktor **5,2** (*851* statt maximal *163*)
* Gesundheitszentren ($z$): Faktor **3,0** (*9 statt 3*)
* Gebietseckpunkte ($g$): Faktor **7,5** (*165* statt maximal *22*)

Die folgende Tabelle hält den Zusammenhang fest zwischen der Zahl der verfügbaren Gesundheitszentren und der Anzahl der Ortschaften, die damit zulässig platziert werden können. Da das Siedlungsgebiet größer ist, tritt erst bei knapp *10* Gesundheitszentren eine Sättigung der möglichen Ortschaftszahl ein. Daher wurden auch mehr Werte als bei den vorgegebenen Siedlungsplänen ermittelt.

| # Gesundheits-<br>zentren | # Ortschaften <br> @ Griechisches Festland |
| --: | --: |
| 0 | 257 |
| 1 | 366 |
| 2 | 420 |
| 3 | 499 |
| 4 | 621 |
| 5 | 707 |
| 6 | 765 |
| 7 | 800 |
| 8 | 838 |
| 9 | 851 |

Die zugehörigen Plankarten sind im Folgenden abgebildet.

| #&nbsp;Zentren | 0 | 1 | 2 | 3 | 4 |
| :--: | :--: | :--: | :--: | :--: | :--: |
| 0+ | ![gk0](output/griechenland/gierig/lauf/karten/257.png) | ![gk1](output/griechenland/gierig/lauf/karten/366.png) | ![gk2](output/griechenland/gierig/lauf/karten/420.png) | ![gk3](output/griechenland/gierig/lauf/karten/499.png) | ![gk4](output/griechenland/gierig/lauf/karten/621.png) |
| 5+ | ![gk5](output/griechenland/gierig/lauf/karten/707.png) | ![gk6](output/griechenland/gierig/lauf/karten/765.png) | ![gk7](output/griechenland/gierig/lauf/karten/800.png) | ![gk8](output/griechenland/gierig/lauf/karten/838.png) | ![gk9](output/griechenland/gierig/lauf/karten/851.png) |

Aus den Plankarten lassen sich folgende Erkenntnisse gewinnen:
* Die *konkaven* Elemente und der *stark zerklüftete* Küstenverlauf des Siedlungsgebiets werden durch den Lösungsansatz sehr gut *berücksichtigt*. Dies zeigt sich z.B. an der Ausnutzung der anspruchsvollen Halbinseln [Chalkidiki](https://de.wikipedia.org/wiki/Chalkidiki) und den [Peloponnes](https://de.wikipedia.org/wiki/Peloponnes).
* Die größere Siedlungsfläche zeigt allerdings *Schwächen* bei der Platzierung der *Gesundheitszentren* auf. Werden diese initial *schlecht* platziert (z.B. in [Thrakien](https://de.wikipedia.org/wiki/Thrakien_(geographische_Region_Griechenlands)) statt in Zentralgriechenland), kann selbst die Punktbewegung der Optimierung dies *nur zum Teil* korrigieren und führt lediglich zu *lokalen Optima*. Dass diese gefunden werden, liegt an der verfolgten Strategie bei der *Bewegung* der Gesundheitszentren. Immer *alle oder keine* zu bewegen, entfällt als Option, da sonst bei den bereits *gut platzierten* Gesundheitszentren sehr wahrscheinlich *Lücken* entstehen würden. Stattdessen berücksichtigt der Optimierer dedizierte Kandidaten, in denen nur genau ein zufälliges Gesundheitszentrum (und keine Ortschaft) bewegt wird.

Zum Abschluss kombiniert das folgende Schaubild für eine variable Anzahl von zulässig platzierten Ortschaften zwei Aspekte: Zum einen wird die Zahl der dafür benötigten Gesundheitszentren angegeben. Zum anderen wird der *Schwierigkeitsgrad* der Hinzunahme einer Ortschaft wie zuvor durch die Zahl der dafür notwendigen *Optimierer-Iterationen* genommen.

![ch-gr-zentren-opiter-pro-orte](docs/gr-zentren-opiter-pro-orte.svg)

# Beispiele

## Optimierer

Die folgenden Kartenreihen zeigen beispielhaft den Verlauf der Optimierung. Bei jeder *Iteration* werden mögliche Kandidaten durch *Punktverschiebung* geschaffen und anhand ihres *Loss* bewertet.

Die lila Punkte sind Ortschaften, die von keinem Gesundheitszentrum abgedeckt werden und zu nah aneinander liegen.

### *Siedler5* bei *128-130* Ortschaften und *1-2* Gesundheitszentren

Dieses Beispiel zeigt, wie Punkte (in diesem Fall das Gesundheitszentrum) erfolgreich *Gebietslücken* überwinden können. Dazu führt im Beispiel die (zufällige) Platzierung der Ortschaften Nummer *129* links unten und *130* links oben.

| vor Ortschaft *129* | Iteration *129.1* | Iteration *130.1* | Iteration *130.2* |
| :--: | :--: | :--: | :--: |
| ![bo2.1](output/siedler5/gierig/lauf/karten/128.png) | ![bo2.2](output/siedler5/gierig/optimierer/2/129/karten/001.png) | ![bo2.3](output/siedler5/gierig/optimierer/2/130/karten/001.png) | ![bo2.4](output/siedler5/gierig/optimierer/2/130/karten/002.png) |

### *Griechisches Festland* bei *813* Ortschaften und *8* Gesundheitszentren

Dieses Beispiel zeigt, wie die Verschiebung eines Gesundheitszentrums über den [Argolischen Golf](https://de.wikipedia.org/wiki/Argolischer_Golf) hinweg zur Abdeckung einiger ungeschützter Ortschaften führt.

| Iteration *1* | Iteration *2* | Iteration *3* |
| :--: | :--: | :--: |
| ![go2.1](output/griechenland/gierig/optimierer/8/813/karten/001.png) | ![go2.2](output/griechenland/gierig/optimierer/8/813/karten/002.png) | ![go2.3](output/griechenland/gierig/optimierer/8/813/karten/003.png) |
| *Loss ≈ 11,405* | *Loss ≈ 2,518* | *Loss=0* |

## Lauf

Die folgenden Kartenreihen zeigen beispielhaft den schrittweisen Aufbau des Besiedlungsplans im *Lauf*. Bei jeder *Iteration* wird eine zusätzliche Ortschaft hinzugefügt und der Plan wird (soweit möglich) durch *Optimierung* zulässig.

### *Siedler 1*

Der Lauf endet bei Iteration *132*. Dieser letzte Plan ist im Feld für *140* dargestellt.

| Iteration | 10 | 20 | 30 | 40 | 50 |
| --: | --: | --: | --: | --: | --: |
| 0+ | ![bl1.10](output/siedler1/gierig/lauf/karten/010.png) | ![bl1.20](output/siedler1/gierig/lauf/karten/020.png) | ![bl1.30](output/siedler1/gierig/lauf/karten/030.png) | ![bl1.40](output/siedler1/gierig/lauf/karten/040.png) | ![bl1.50](output/siedler1/gierig/lauf/karten/050.png) |
| 50+ | ![bl1.60](output/siedler1/gierig/lauf/karten/060.png) | ![bl1.70](output/siedler1/gierig/lauf/karten/070.png) | ![bl1.80](output/siedler1/gierig/lauf/karten/080.png) | ![bl1.90](output/siedler1/gierig/lauf/karten/090.png) | ![bl1.100](output/siedler1/gierig/lauf/karten/100.png) |
| 100+ | ![bl1.110](output/siedler1/gierig/lauf/karten/110.png) | ![bl1.120](output/siedler1/gierig/lauf/karten/120.png) | ![bl1.130](output/siedler1/gierig/lauf/karten/130.png) | ![bl1.133](output/siedler1/gierig/lauf/karten/132.png) | |

### *Griechisches Festland*

Der Lauf endet bei Iteration *851*. Dieser letzte Plan ist im Feld für *860* dargestellt.

| Iteration | 0 | 20 | 40 | 60 | 80 |
| --: | --: | --: | --: | --: | --: |
| 0+ | ![gl1.0](output/griechenland/gierig/lauf/karten/000.png) | ![gl1.20](output/griechenland/gierig/lauf/karten/020.png) | ![gl1.40](output/griechenland/gierig/lauf/karten/040.png) | ![gl1.60](output/griechenland/gierig/lauf/karten/060.png) | ![gl1.80](output/griechenland/gierig/lauf/karten/080.png) |
| 100+ | ![gl1.100](output/griechenland/gierig/lauf/karten/100.png) | ![gl1.120](output/griechenland/gierig/lauf/karten/120.png) | ![gl1.140](output/griechenland/gierig/lauf/karten/140.png) | ![gl1.160](output/griechenland/gierig/lauf/karten/160.png) | ![gl1.180](output/griechenland/gierig/lauf/karten/180.png) |
| 200+ | ![gl1.200](output/griechenland/gierig/lauf/karten/200.png) | ![gl1.220](output/griechenland/gierig/lauf/karten/220.png) | ![gl1.240](output/griechenland/gierig/lauf/karten/240.png) | ![gl1.260](output/griechenland/gierig/lauf/karten/260.png) | ![gl1.280](output/griechenland/gierig/lauf/karten/280.png) |
| 300+ | ![gl1.300](output/griechenland/gierig/lauf/karten/300.png) | ![gl1.30](output/griechenland/gierig/lauf/karten/320.png) | ![gl1.340](output/griechenland/gierig/lauf/karten/340.png) | ![gl1.360](output/griechenland/gierig/lauf/karten/360.png) | ![gl1.380](output/griechenland/gierig/lauf/karten/380.png) |
| 400+ | ![gl1.400](output/griechenland/gierig/lauf/karten/400.png) | ![gl1.420](output/griechenland/gierig/lauf/karten/420.png) | ![gl1.440](output/griechenland/gierig/lauf/karten/440.png) | ![gl1.460](output/griechenland/gierig/lauf/karten/460.png) | ![gl1.480](output/griechenland/gierig/lauf/karten/480.png) |
| 500+ | ![gl1.500](output/griechenland/gierig/lauf/karten/500.png) | ![gl1.520](output/griechenland/gierig/lauf/karten/520.png) | ![gl1.540](output/griechenland/gierig/lauf/karten/540.png) | ![gl1.560](output/griechenland/gierig/lauf/karten/560.png) | ![gl1.580](output/griechenland/gierig/lauf/karten/580.png) |
| 600+ | ![gl1.600](output/griechenland/gierig/lauf/karten/600.png) | ![gl1.620](output/griechenland/gierig/lauf/karten/620.png) | ![gl1.640](output/griechenland/gierig/lauf/karten/640.png) | ![gl1.660](output/griechenland/gierig/lauf/karten/660.png) | ![gl1.680](output/griechenland/gierig/lauf/karten/680.png) |
| 700+ | ![gl1.700](output/griechenland/gierig/lauf/karten/700.png) | ![gl1.720](output/griechenland/gierig/lauf/karten/720.png) | ![gl1.740](output/griechenland/gierig/lauf/karten/740.png) | ![gl1.760](output/griechenland/gierig/lauf/karten/760.png) | ![gl1.780](output/griechenland/gierig/lauf/karten/780.png) |
| 800+ | ![gl1.800](output/griechenland/gierig/lauf/karten/800.png) | ![gl1.820](output/griechenland/gierig/lauf/karten/820.png) | ![gl1.840](output/griechenland/gierig/lauf/karten/840.png) | ![gl1.851](output/griechenland/gierig/lauf/karten/851.png) |  |
