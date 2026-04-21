# Konzept: Synthetische Datengenerierung für Wartungs- und Prüfungsmanagement

Ich habe mich bei meinem Konzept am Seed-Guided Generation Prompt von "DocGenie: A Framework for High-Fidelity Synthetic Document Generation via Seed-Guided Multimodal LLM and Document-Aware Evaluation" (https://openreview.net/forum?id=cT5v6GjdsH, Published: May 2025) orientiert, der die synthetische Dokumentgenerierung mit Seed-Dokumenten und einem multimodalen LLM kombiniert, um sowohl den Inhalt als auch die Struktur zu generieren.

## 1. Analyse der vorhandenen Dokumente

Vorhandene Datenpunkte nach Inhalt und Aufbau analysieren.
- Vorhandene Dokumente  (PDF / DOCX) als Seed Documents

## 2. Variationsdimensionen definieren

- Dokumententyp (Wartungsvertrag vs. Wartungsprotokoll)
- Anlagentyp (z.B. Wärmepumpe, Rauchmelder, etc.)
- Vorhandenen Mängel (keine, mittlere, größere Mängel) [Noch nicht im Prototyp umgesetzt!]
- Grundlegende Dokumentenstruktur (Anschrift, Unterschrift, etc.) als Baseline Requirements, die für jeden generierten Datenpunkt vorhanden sein sollen (unterschiedlich für Vertrag vs. Protokoll)
- Layout (Tabellen, Checkboxen, Freitextfelder, etc.)

## 4. Daten generieren

Text und Struktur generieren:

- Synthetic Data Generation duch parametrisiertes Prompt Engineering (Claude Sonnet 4) mit Variationsdimensionen als Steuerungsparameter
- Generierung von HTML-Strukturen
```
1. <HTML>...Solution #1...</HTML>
2. <HTML>...Solution #2...</HTML>
   ...
```
- Mehrere HTML-Dokumente in einem Prompt generieren; Unterschiede zwischen den Dokumenten sicherstellen
- Seeds: Vorhandene Dokumente als Basis für Inhalt, Stil und Struktur (jeweils unterschiedliche Seed Dokumente für Vertrag vs. Protokoll)

## 5. Layout rendern
- HTML-Struktur in PDF umwandeln

## 6. Evaluation

- Similarity zwichen generierten Dokumenten und Seed-Dokumenten berechnen (z.B. mit FID-Layout, Modifikation der Frechet Inception
Distance). [NICHT im Prototype umgesetzt!]

## Weitere Möglichkeiten
Eine andere Möglichkeit wäre die Dokumentstruktur zu analysieren und JSON-Daten zu erstellen (z.B. regelbasiert und Freitexte mit LLM), die dann in einem Template gerendert werden. Da aber eine Varianz im Dokumentenlayout auch ein Punkt für möglichst "echte" Daten ist, habe ich mich für die direkte Generierung von HTML-Layouts entschieden, um auch möglichst verschiedene Layoutstrukturen abzubilden.

Ein weiterer Ansatz wäre die Datenpunkte direkt mit einem generativen Modell zu erstellen, das auf den Dokument-Daten trainiert wurde (nur wenn mehr als 4 Trainingsdaten vorhanden sind). Zudem könnten man die Dokumente mit visuellen Elementen (Logos etc.) und Diffusions Modellen (z.B. für Unterschriften) noch realistischer machen ("Controllable Synthetic Document Generation with VLMs and Handwriting Diffusion" (https://arxiv.org/pdf/2602.21824)).