# Aequivalenz & Repräsentanten

## Quadratisch ohne Zielfeld

Die folgenden Schulhoefe sind aequivalent, da sie sich aus einer Sequenz von Spiegelungen ergeben. Ihr Repraesentant ist der String `9,2,7,1,4,6,5,3,8@3,3`, der sich aus dem Maximum des lexikografischen Vergleichs ergibt. Andere Vergleiche (Minimum, Einzelfeldvergleich in `int`) waeren auch moeglich. Entscheidend ist lediglich, dass diese Berechnung immer auf dieselben Art und Weise erfolgt und fuer alle aequivalenten Schulhoefe zum selben Ergebnis kommt.

Schulhof, aus dem sich der Repraesentant ergibt:
```
-------
|9|2|7|
-------
|1|4|6|
-------
|5|3|8|
-------
```

Schulhof, der durch **Diagonalspiegelung** zum Repraesentanten gelangt:
```
-------
|9|1|5|
-------
|2|4|3|
-------
|7|6|8|
-------
```

Schulhof, der durch **Horizontalspiegelung** zum Repraesentanten gelangt:
```
-------
|7|2|9|
-------
|6|4|1|
-------
|8|3|5|
-------
```

Schulhof, der durch **Vertikalspiegelung** zum Repraesentanten gelangt:
```
-------
|5|3|8|
-------
|1|4|6|
-------
|9|2|7|
-------
```

Schulhof, der durch **Horizontal- und Vertikalspiegelung** zum Repraesentanten gelangt:
```
-------
|8|3|5|
-------
|6|4|1|
-------
|7|2|9|
-------
```

Schulhof, der durch **Vertikal und Diagonalspiegelung** zum Repraesentanten gelangt:
```
-------
|7|6|8|
-------
|2|4|3|
-------
|9|1|5|
-------
```

Schulhof, der durch **Horizontal- und Diagonalspiegelung** zum Repraesentanten gelangt:
```
-------
|5|1|9|
-------
|3|4|2|
-------
|8|6|7|
-------
```

Schulhof, der durch **Horizontal-, Vertikal- und Diagonalspiegelung** zum Repraesentanten gelangt:
```
-------
|8|6|7|
-------
|3|4|2|
-------
|5|1|9|
-------
```

## Rechteck ohne Zielfeld

Bei nicht quadratischen Schulhoefen entfaellt die Moeglichkeit der Diagonalspiegelungen. In einer Aequivalenzklasse sind dann jeweils vier Schulhoefe.

Schulhof, aus dem sich der Repraesentant `9,2,7,0,1,4,6,5,5,3,8,2@4,3` ergibt:
```
---------
|9|2|7|0|
---------
|1|4|6|5|
---------
|5|3|8|2|
---------
```

Schulhof, der durch **Horizontalspiegelung** zum Repraesentanten gelangt:
```
---------
|0|7|2|9|
---------
|5|6|4|1|
---------
|2|8|3|5|
---------
```

Schulhof, der durch **Vertikalspiegelung** zum Repraesentanten gelangt:
```
---------
|5|3|8|2|
---------
|1|4|6|5|
---------
|9|2|7|0|
---------
```

Schulhof, der durch **Horizontal- und Vertikalspiegelung** zum Repraesentanten gelangt:
```
---------
|2|8|3|5|
---------
|5|6|4|1|
---------
|0|7|2|9|
---------
```

## Mit Zielfeld

Wenn ein Zielfeld fest vorgegeben ist, darf es sich durch die Spiegelungen nicht veraendern. Dies ist nicht nur gegeben, wenn es auf den angewendeten Spiegelachsen liegt. Zum Beispiel sind beide folgenden Schulhoefe aequivalent, da der erste sich durch Horizontal-, Vertikal- und Diagonalspiegelung aus dem zweiten ergibt.

```
---------        ---------
|9|2|7|0|        |2|4|5|0|
---------        ---------
|1|4‖6‖5|        |8|9‖6‖7|
---------        ---------
|3|8|9|4|        |3|8|4|2|
---------        ---------
|5|3|8|2|        |5|3|1|9|
---------        ---------
```

# Blase-Operationen

## Vervollstaendigung der Aufgabenstellung

Mehrere Randfaelle sind in der Aufgabenstellung nicht abgedeckt. Dieser Abschnitt zeigt ihre Definition. Dabei wird davon ausgegangen, dass
* der Schulhof in alle Richtungen umzaeunt ist,
* kein Rueckstoß aus dem Blasen gegen den Zaun entsteht.

Beim Blasen entlang des Rands gibt es am Zaun keinen Seitenverlust:
```
-----------------             -----------------
| > | 40| 50| 60|             | > |  0| 81| 65|
-----------------     ==>     -----------------
|  0| 10| 20| 30|             |  0| 10| 24| 30|
-----------------             -----------------
```

Beim Blasen zwei Felder vor dem Zaun gibt es keinen "Ueberlauf" nach hinten:
```
-----------------             -----------------
|  0| > | 50| 60|             |  0| > |  0|105|
-----------------     ==>     -----------------
|  0| 10| 20| 30|             |  0| 10| 20| 35|
-----------------             -----------------
```

Das Blasen ein Feld vor dem Zaun hat keine Wirkung:
```
-----------------             -----------------
|  0| 40| 50| 60|             |  0| 40| 50| 60|
-----------------     ==>     -----------------
|  0| ^ | 20| 30|             |  0| ^ | 20| 30|
-----------------             -----------------
```

Ebenso wenig das Blasen direkt vor dem Zaun:
```
-----------------             -----------------
|  0| 40| 50| 60|             |  0| 40| 50| 60|
-----------------     ==>     -----------------
|  0| v | 20| 30|             |  0| v | 20| 30|
-----------------             -----------------
```

## Potenziell veraendernde Blase-Operationen

Fuer einen $5*5$ Schulhof sind alle $60$ Blaseoperationen gezeigt, die das Potential haben, die Laubsitutation auf dem Schulhof zu veraendern. Es wird nur von Potential gesprochen, da eine tatsaechliche Veraenderung natuerlich von der Laubsituation abhaengig ist (liegt zum Beispiel ueberhaupt kein Laub, wird keine Operation zu einer Veraenderung fuehren).

```
---------------------
|   |   |   |   |   |
|  >|  >|< >|<  |<  |
| v | v | v | v | v |
---------------------
|   |   |   |   |   |
|  >|  >|< >|<  |<  |
| v | v | v | v | v |
---------------------
| ^ | ^ | ^ | ^ | ^ |
|  >|  >|< >|<  |<  |
| v | v | v | v | v |
---------------------
| ^ | ^ | ^ | ^ | ^ |
|  >|  >|< >|<  |<  |
|   |   |   |   |   |
---------------------
| ^ | ^ | ^ | ^ | ^ |
|  >|  >|< >|<  |<  |
|   |   |   |   |   |
---------------------
```