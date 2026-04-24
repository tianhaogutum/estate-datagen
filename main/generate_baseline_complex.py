"""
Generator for scenario_baseline_complex:
  2 EconomicUnits × 2 Buildings × 2 Devices × 2 Contracts × 2 Protocols
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "output_scenarios" / "scenario_baseline_complex"

# ─────────────────────────────────────────────────────────────────────────────
# Scenario data definition
# Each contract has 2 protocols.
# Layout: 2 units → 2 buildings → 2 devices → 2 contracts → 2 protocols
# ─────────────────────────────────────────────────────────────────────────────

SCENARIO = [
    # ══ Economic Unit 1 ═══════════════════════════════════════════════════════
    {
        "unit_name": "Stadtwerke München Immobilien GmbH",
        "unit_phone": "+49 89 2361000",
        "unit_contact": "Dr. Petra Hoffmann",
        "unit_sign_city": "München",
        "buildings": [
            # ── Building 1 ──────────────────────────────────────────────────
            {
                "address": "Leopoldstraße 18, 80802 München",
                "city": "München",
                "type": "Bürogebäude",
                "devices": [
                    # ·· Device 1 ············································
                    {
                        "type": "Klimaanlage (VRF-System)",
                        "manufacturer": "Mitsubishi Electric",
                        "model": "City Multi R2",
                        "serial": "ME-CMR2-2019-00214",
                        "contracts": [
                            {
                                "id": "c1b1d1v1",
                                "provider": "KlimaService Bayern GmbH",
                                "provider_addr": "Gewerbepark Süd 12, 85521 Ottobrunn",
                                "provider_phone": "+49 89 6073400",
                                "provider_city": "Ottobrunn",
                                "provider_email": "service@klimaservice-bayern.de",
                                "provider_technician": "Michael Rauer",
                                "sign_date": "2019-12-01",
                                "start": "2020-01-01",
                                "end": "2022-12-31",
                                "frequency": "Jährlich",
                                "cost": 1200.0,
                                "protocols": [
                                    {
                                        "date": "2020-09-14",
                                        "result": "Wartung erfolgreich abgeschlossen – Anlage betriebsbereit",
                                        "remarks": "Alle vier Innengeräte in einwandfreiem Zustand. Keine Mängel festgestellt.",
                                    },
                                    {
                                        "date": "2021-09-08",
                                        "result": "Leichte Verschmutzung im Wärmetauscher behoben – Anlage betriebsbereit",
                                        "remarks": "Wärmetauscher gereinigt. Kältemittelkreislauf auf Dichtigkeit geprüft – kein Leck.",
                                    },
                                ],
                            },
                            {
                                "id": "c1b1d1v2",
                                "provider": "TechAir Kälte- und Klimatechnik GmbH",
                                "provider_addr": "Industriestraße 77, 80939 München",
                                "provider_phone": "+49 89 3214570",
                                "provider_city": "München",
                                "provider_email": "wartung@techair-klima.de",
                                "provider_technician": "Sandra Weiß",
                                "sign_date": "2022-11-15",
                                "start": "2023-01-01",
                                "end": "2025-12-31",
                                "frequency": "Jährlich",
                                "cost": 1480.0,
                                "protocols": [
                                    {
                                        "date": "2023-09-06",
                                        "result": "Erstinspektion und Übergabe – Anlage betriebsbereit",
                                        "remarks": "Übernahmeinspektion nach Vertragswechsel. Anlage in gutem Zustand übergeben.",
                                    },
                                    {
                                        "date": "2024-09-11",
                                        "result": "Jahreswartung erfolgreich abgeschlossen – Anlage betriebsbereit",
                                        "remarks": "Alle Filter gewechselt. Kältemittelfüllmenge geprüft – kein Nachfüllen erforderlich.",
                                    },
                                ],
                            },
                        ],
                    },
                    # ·· Device 2 ············································
                    {
                        "type": "Personenaufzug",
                        "manufacturer": "ThyssenKrupp Elevator AG",
                        "model": "Evolution 200",
                        "serial": "TKE-EV200-2017-00831",
                        "contracts": [
                            {
                                "id": "c1b1d2v1",
                                "provider": "ThyssenKrupp Aufzüge GmbH",
                                "provider_addr": "Helfmann-Park 5, 65760 Eschborn",
                                "provider_phone": "+49 6196 9840",
                                "provider_city": "Eschborn",
                                "provider_email": "aufzugservice@thyssenkrupp.com",
                                "provider_technician": "Jörg Neumann",
                                "sign_date": "2018-06-01",
                                "start": "2018-07-01",
                                "end": "2021-06-30",
                                "frequency": "Halbjährlich",
                                "cost": 2400.0,
                                "protocols": [
                                    {
                                        "date": "2019-03-20",
                                        "result": "TÜV-Prüfung bestanden – Aufzug betriebsbereit",
                                        "remarks": "Sicherheitsprüfung gem. BetrSichV durchgeführt. Alle Sicherheitseinrichtungen funktionsfähig.",
                                    },
                                    {
                                        "date": "2020-10-15",
                                        "result": "Wartung erfolgreich – geringfügige Schmierung erneuert",
                                        "remarks": "Seilschmierung erneuert, Türverriegelung neu eingestellt. Betrieb sicher.",
                                    },
                                ],
                            },
                            {
                                "id": "c1b1d2v2",
                                "provider": "ThyssenKrupp Aufzüge GmbH",
                                "provider_addr": "Helfmann-Park 5, 65760 Eschborn",
                                "provider_phone": "+49 6196 9840",
                                "provider_city": "Eschborn",
                                "provider_email": "aufzugservice@thyssenkrupp.com",
                                "provider_technician": "Jörg Neumann",
                                "sign_date": "2021-05-10",
                                "start": "2021-07-01",
                                "end": "2024-06-30",
                                "frequency": "Halbjährlich",
                                "cost": 2800.0,
                                "protocols": [
                                    {
                                        "date": "2022-04-05",
                                        "result": "Halbjahreswartung und TÜV-Inspektion – Betrieb freigegeben",
                                        "remarks": "Hydraulik und Steuereinheit geprüft. Nächste Hauptprüfung Oktober 2022.",
                                    },
                                    {
                                        "date": "2023-10-12",
                                        "result": "Wartung erfolgreich – Fangvorrichtung neu kalibriert",
                                        "remarks": "Fangvorrichtung überprüft und kalibriert. Steuerplatine auf Firmware-Update geprüft – aktuell.",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            # ── Building 2 ──────────────────────────────────────────────────
            {
                "address": "Maximilianstraße 7, 80539 München",
                "city": "München",
                "type": "Geschäftsgebäude",
                "devices": [
                    # ·· Device 1 ············································
                    {
                        "type": "Heizungsanlage (Gas-Brennwertkessel)",
                        "manufacturer": "Viessmann",
                        "model": "Vitodens 300-W",
                        "serial": "VTD300W-2018-05512",
                        "contracts": [
                            {
                                "id": "c1b2d1v1",
                                "provider": "Viessmann Kundendienst GmbH",
                                "provider_addr": "Viessmannstraße 1, 35108 Allendorf",
                                "provider_phone": "+49 6452 7090",
                                "provider_city": "Allendorf",
                                "provider_email": "service@viessmann.com",
                                "provider_technician": "Klaus Bauer",
                                "sign_date": "2020-09-01",
                                "start": "2020-10-01",
                                "end": "2023-09-30",
                                "frequency": "Jährlich",
                                "cost": 890.0,
                                "protocols": [
                                    {
                                        "date": "2021-10-05",
                                        "result": "Jahreswartung erfolgreich – Anlage betriebsbereit",
                                        "remarks": "Brenner gereinigt, Wärmetauscher gespült. CO₂-Wert im Normbereich.",
                                    },
                                    {
                                        "date": "2022-10-12",
                                        "result": "Kleinere Einstellung vorgenommen – Anlage betriebsbereit",
                                        "remarks": "Brennereinstellung optimiert. Abgaswert leicht außerhalb Toleranz, korrigiert.",
                                    },
                                ],
                            },
                            {
                                "id": "c1b2d1v2",
                                "provider": "Viessmann Kundendienst GmbH",
                                "provider_addr": "Viessmannstraße 1, 35108 Allendorf",
                                "provider_phone": "+49 6452 7090",
                                "provider_city": "Allendorf",
                                "provider_email": "service@viessmann.com",
                                "provider_technician": "Klaus Bauer",
                                "sign_date": "2023-08-15",
                                "start": "2023-10-01",
                                "end": "2026-09-30",
                                "frequency": "Jährlich",
                                "cost": 980.0,
                                "protocols": [
                                    {
                                        "date": "2023-10-09",
                                        "result": "Übergabe-Inspektion und Jahreswartung – Anlage betriebsbereit",
                                        "remarks": "Übergabeinspektion nach Vertragsverlängerung. Dichtheitsprüfung unauffällig.",
                                    },
                                    {
                                        "date": "2024-10-14",
                                        "result": "Jahreswartung erfolgreich abgeschlossen – Anlage betriebsbereit",
                                        "remarks": "Ionisierungselektrode erneuert. Betriebsstunden: 14.820 h.",
                                    },
                                ],
                            },
                        ],
                    },
                    # ·· Device 2 ············································
                    {
                        "type": "Lüftungsanlage (RLT-Anlage)",
                        "manufacturer": "Trox GmbH",
                        "model": "ECFD 800",
                        "serial": "TROX-ECFD-2019-01129",
                        "contracts": [
                            {
                                "id": "c1b2d2v1",
                                "provider": "LufttechnikNord GmbH",
                                "provider_addr": "Siemensstraße 14, 22113 Hamburg",
                                "provider_phone": "+49 40 7330880",
                                "provider_city": "Hamburg",
                                "provider_email": "service@lufttechniknord.de",
                                "provider_technician": "Andreas Schröder",
                                "sign_date": "2020-03-01",
                                "start": "2020-04-01",
                                "end": "2023-03-31",
                                "frequency": "Halbjährlich",
                                "cost": 1650.0,
                                "protocols": [
                                    {
                                        "date": "2021-04-20",
                                        "result": "Halbjähreswartung – Filterwechsel durchgeführt",
                                        "remarks": "G4-Taschenfilter getauscht. Luftmengenmessung: Sollwert ±3 %.",
                                    },
                                    {
                                        "date": "2022-10-25",
                                        "result": "Halbjahreswartung – Anlage betriebsbereit",
                                        "remarks": "F7-Feinfilter gewechselt. Wärmerückgewinnungsrotor gereinigt.",
                                    },
                                ],
                            },
                            {
                                "id": "c1b2d2v2",
                                "provider": "LufttechnikNord GmbH",
                                "provider_addr": "Siemensstraße 14, 22113 Hamburg",
                                "provider_phone": "+49 40 7330880",
                                "provider_city": "Hamburg",
                                "provider_email": "service@lufttechniknord.de",
                                "provider_technician": "Andreas Schröder",
                                "sign_date": "2023-02-20",
                                "start": "2023-04-01",
                                "end": "2026-03-31",
                                "frequency": "Halbjährlich",
                                "cost": 1820.0,
                                "protocols": [
                                    {
                                        "date": "2023-11-08",
                                        "result": "Halbjahreswartung erfolgreich – Anlage betriebsbereit",
                                        "remarks": "Antriebsriemen der Ventilatoren geprüft. Kein erhöhter Verschleiß. Nächste Wartung: Mai 2024.",
                                    },
                                    {
                                        "date": "2024-05-15",
                                        "result": "Halbjahreswartung erfolgreich – Anlage betriebsbereit",
                                        "remarks": "Kondensatwanne gespült und desinfiziert. Hygieneinspektion gem. VDI 6022 bestanden.",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # ══ Economic Unit 2 ═══════════════════════════════════════════════════════
    {
        "unit_name": "Wohnbaugesellschaft Nordrhein GmbH",
        "unit_phone": "+49 211 8370420",
        "unit_contact": "Thomas Bergmann",
        "unit_sign_city": "Düsseldorf",
        "buildings": [
            # ── Building 1 ──────────────────────────────────────────────────
            {
                "address": "Königsallee 42, 40212 Düsseldorf",
                "city": "Düsseldorf",
                "type": "Wohngebäude",
                "devices": [
                    # ·· Device 1 ············································
                    {
                        "type": "Wärmepumpe (Luft-Wasser)",
                        "manufacturer": "Viessmann",
                        "model": "Vitocal 250-A",
                        "serial": "VTC250A-2021-00743",
                        "contracts": [
                            {
                                "id": "c2b1d1v1",
                                "provider": "WärmetechnikRuhr GmbH",
                                "provider_addr": "Ruhrdeich 9, 45478 Mülheim an der Ruhr",
                                "provider_phone": "+49 208 4429010",
                                "provider_city": "Mülheim an der Ruhr",
                                "provider_email": "service@waermetechnikruhr.de",
                                "provider_technician": "Frank Richter",
                                "sign_date": "2021-03-10",
                                "start": "2021-04-01",
                                "end": "2024-03-31",
                                "frequency": "Jährlich",
                                "cost": 1100.0,
                                "protocols": [
                                    {
                                        "date": "2022-05-18",
                                        "result": "Jahreswartung erfolgreich – Anlage betriebsbereit",
                                        "remarks": "COP-Messung: 3,8. Kältemittelkreislauf dicht. Kondensatwanne gereinigt.",
                                    },
                                    {
                                        "date": "2023-05-22",
                                        "result": "Kältemittel R-32 nachgefüllt – Anlage betriebsbereit",
                                        "remarks": "Geringe Leckage an Verschraubung behoben, 180 g R-32 nachgefüllt. Leckageprotokoll erstellt.",
                                    },
                                ],
                            },
                            {
                                "id": "c2b1d1v2",
                                "provider": "WärmetechnikRuhr GmbH",
                                "provider_addr": "Ruhrdeich 9, 45478 Mülheim an der Ruhr",
                                "provider_phone": "+49 208 4429010",
                                "provider_city": "Mülheim an der Ruhr",
                                "provider_email": "service@waermetechnikruhr.de",
                                "provider_technician": "Frank Richter",
                                "sign_date": "2024-02-01",
                                "start": "2024-04-01",
                                "end": "2027-03-31",
                                "frequency": "Jährlich",
                                "cost": 1280.0,
                                "protocols": [
                                    {
                                        "date": "2024-05-16",
                                        "result": "Erstinspektion nach Vertragsverlängerung – Anlage betriebsbereit",
                                        "remarks": "Übernahmeinspektion: Anlage in einwandfreiem Zustand. Neue Inspektionskarte ausgestellt.",
                                    },
                                    {
                                        "date": "2025-05-20",
                                        "result": "Jahreswartung erfolgreich – Anlage betriebsbereit",
                                        "remarks": "Wärmequellenkreislauf gespült. Effizienzprüfung: COP 4,1. Kein Handlungsbedarf.",
                                    },
                                ],
                            },
                        ],
                    },
                    # ·· Device 2 ············································
                    {
                        "type": "Brandmeldeanlage",
                        "manufacturer": "Bosch Security Systems",
                        "model": "FPA-5000",
                        "serial": "BSS-FPA5000-2019-08821",
                        "contracts": [
                            {
                                "id": "c2b1d2v1",
                                "provider": "SecureFire Sicherheitstechnik GmbH",
                                "provider_addr": "Sicherheitsring 3, 40549 Düsseldorf",
                                "provider_phone": "+49 211 5034700",
                                "provider_city": "Düsseldorf",
                                "provider_email": "wartung@securefire.de",
                                "provider_technician": "Stefan Keller",
                                "sign_date": "2019-11-01",
                                "start": "2019-12-01",
                                "end": "2022-11-30",
                                "frequency": "Jährlich",
                                "cost": 750.0,
                                "protocols": [
                                    {
                                        "date": "2020-12-08",
                                        "result": "Jahresinspektion bestanden – Anlage betriebsbereit",
                                        "remarks": "Alle 42 Rauchmelder getestet. Zentrale und Alarmierungseinrichtungen funktionsfähig.",
                                    },
                                    {
                                        "date": "2021-12-14",
                                        "result": "Funktionstest aller Melder – keine Mängel",
                                        "remarks": "Ersatzbatterien in 6 Meldern getauscht. Protokoll gem. DIN 14675 erstellt.",
                                    },
                                ],
                            },
                            {
                                "id": "c2b1d2v2",
                                "provider": "SecureFire Sicherheitstechnik GmbH",
                                "provider_addr": "Sicherheitsring 3, 40549 Düsseldorf",
                                "provider_phone": "+49 211 5034700",
                                "provider_city": "Düsseldorf",
                                "provider_email": "wartung@securefire.de",
                                "provider_technician": "Stefan Keller",
                                "sign_date": "2022-10-10",
                                "start": "2022-12-01",
                                "end": "2025-11-30",
                                "frequency": "Jährlich",
                                "cost": 820.0,
                                "protocols": [
                                    {
                                        "date": "2023-12-05",
                                        "result": "Jahreswartung bestanden – Anlage betriebsbereit",
                                        "remarks": "7 Rauchmelder der Baureihe FDO 221 ausgetauscht (Serienabruf). Prüfbescheinigung ausgestellt.",
                                    },
                                    {
                                        "date": "2024-12-10",
                                        "result": "Jahresinspektion erfolgreich – alle Melder betriebsbereit",
                                        "remarks": "Übertragungseinrichtung zur Feuerwehr-Leitstelle geprüft und freigegeben.",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            # ── Building 2 ──────────────────────────────────────────────────
            {
                "address": "Berliner Allee 15, 40212 Düsseldorf",
                "city": "Düsseldorf",
                "type": "Wohngebäude",
                "devices": [
                    # ·· Device 1 ············································
                    {
                        "type": "Sprinkleranlage",
                        "manufacturer": "Minimax GmbH",
                        "model": "Viking Sprinkler VK302",
                        "serial": "MMX-VK302-2018-00559",
                        "contracts": [
                            {
                                "id": "c2b2d1v1",
                                "provider": "Minimax Mobile Services GmbH & Co. KG",
                                "provider_addr": "Industriestraße 10–12, 23840 Bad Oldesloe",
                                "provider_phone": "+49 4531 8030",
                                "provider_city": "Bad Oldesloe",
                                "provider_email": "service@minimax.de",
                                "provider_technician": "Nina Brandt",
                                "sign_date": "2018-07-01",
                                "start": "2018-08-01",
                                "end": "2021-07-31",
                                "frequency": "Halbjährlich",
                                "cost": 1900.0,
                                "protocols": [
                                    {
                                        "date": "2019-08-20",
                                        "result": "Halbjahreswartung – Drucktest bestanden",
                                        "remarks": "Netzwerkdrucktest: 14,2 bar. Alle Sprinklerköpfe auf Korrosion geprüft – einwandfrei.",
                                    },
                                    {
                                        "date": "2020-09-15",
                                        "result": "Halbjahresinspektion bestanden – Anlage betriebsbereit",
                                        "remarks": "Wasserversorgung und Alarmventilgruppen geprüft. 3 Sprinklerköpfe vorsorglich ersetzt.",
                                    },
                                ],
                            },
                            {
                                "id": "c2b2d1v2",
                                "provider": "Minimax Mobile Services GmbH & Co. KG",
                                "provider_addr": "Industriestraße 10–12, 23840 Bad Oldesloe",
                                "provider_phone": "+49 4531 8030",
                                "provider_city": "Bad Oldesloe",
                                "provider_email": "service@minimax.de",
                                "provider_technician": "Nina Brandt",
                                "sign_date": "2021-06-01",
                                "start": "2021-08-01",
                                "end": "2024-07-31",
                                "frequency": "Halbjährlich",
                                "cost": 2100.0,
                                "protocols": [
                                    {
                                        "date": "2022-08-17",
                                        "result": "Halbjahreswartung erfolgreich – Anlage betriebsbereit",
                                        "remarks": "Pumpengruppe geprüft, Laufzeit und Förderdruck innerhalb Sollwerte.",
                                    },
                                    {
                                        "date": "2023-09-03",
                                        "result": "Halbjahresinspektion – geringfügige Instandsetzung durchgeführt",
                                        "remarks": "Alarmventil-Dichtung erneuert. Betrieb nach Prüfung wieder freigegeben.",
                                    },
                                ],
                            },
                        ],
                    },
                    # ·· Device 2 ············································
                    {
                        "type": "Elektrische Anlage (Niederspannung)",
                        "manufacturer": "Siemens AG",
                        "model": "SENTRON 3VA",
                        "serial": "SIE-3VA-2020-11047",
                        "contracts": [
                            {
                                "id": "c2b2d2v1",
                                "provider": "ElektroProfis GmbH & Co. KG",
                                "provider_addr": "Stromweg 22, 40474 Düsseldorf",
                                "provider_phone": "+49 211 6620910",
                                "provider_city": "Düsseldorf",
                                "provider_email": "pruefdienst@elektroprofis.de",
                                "provider_technician": "Ralf Zimmermann",
                                "sign_date": "2021-01-10",
                                "start": "2021-03-01",
                                "end": "2024-02-29",
                                "frequency": "Jährlich",
                                "cost": 650.0,
                                "protocols": [
                                    {
                                        "date": "2022-04-18",
                                        "result": "DGUV V3-Prüfung bestanden – Anlage betriebssicher",
                                        "remarks": "Isolationswiderstand: ≥ 1 MΩ. Alle Schutzleiterwiderstände unter 0,3 Ω. Prüfprotokoll gem. DIN VDE 0105-100.",
                                    },
                                    {
                                        "date": "2023-04-21",
                                        "result": "Sicherheitsprüfung bestanden – keine Mängel",
                                        "remarks": "Überspannungsschutz (SPD Typ 2) geprüft und für in Ordnung befunden. Nächste Prüfung: April 2024.",
                                    },
                                ],
                            },
                            {
                                "id": "c2b2d2v2",
                                "provider": "ElektroProfis GmbH & Co. KG",
                                "provider_addr": "Stromweg 22, 40474 Düsseldorf",
                                "provider_phone": "+49 211 6620910",
                                "provider_city": "Düsseldorf",
                                "provider_email": "pruefdienst@elektroprofis.de",
                                "provider_technician": "Ralf Zimmermann",
                                "sign_date": "2024-01-15",
                                "start": "2024-03-01",
                                "end": "2027-02-28",
                                "frequency": "Jährlich",
                                "cost": 720.0,
                                "protocols": [
                                    {
                                        "date": "2024-04-17",
                                        "result": "DGUV V3-Jahresprüfung bestanden – Anlage betriebssicher",
                                        "remarks": "Alle ortsveränderlichen Betriebsmittel geprüft. 2 defekte Steckdosen ausgetauscht.",
                                    },
                                    {
                                        "date": "2025-04-22",
                                        "result": "Jahresprüfung erfolgreich – keine Beanstandungen",
                                        "remarks": "FI-Schutzschalter getestet (Auslösezeit < 300 ms). Erdungsanlage gemessen – Widerstand 1,8 Ω.",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Builder functions
# ─────────────────────────────────────────────────────────────────────────────


def _make_contract(unit: dict, building: dict, device: dict, contract: dict) -> dict:
    c = contract
    d = device
    return {
        "meta": {
            "entity": "MaintenanceContract",
            "field_values": {
                "id": c["id"],
                "building_id": None,
                "device_type": d["type"],
                "service_provider_id": None,
                "contract_date": c["sign_date"],
                "contract_start": c["start"],
                "contract_end": c["end"],
                "termination_period_months": "3 Monate",
                "termination_deadline_rule": None,
                "maintenance_frequency": c["frequency"],
                "cost_per_maintenance": c["cost"],
            },
        },
        "required": {
            "Anlagentyp": {
                "Typ": d["type"],
                "Hersteller": d["manufacturer"],
                "Modell": d["model"],
                "Anzahl": "1",
            },
            "Auftraggeber": {
                "Name": unit["unit_name"],
                "Anschrift": building["address"],
                "Telefon": unit["unit_phone"],
            },
            "Auftragnehmer": {
                "Firma": c["provider"],
                "Anschrift": c["provider_addr"],
                "Telefon": c["provider_phone"],
            },
            "Objekt_der_Wartung": {
                "Adresse": building["address"],
            },
            "Gegenstand_des_Vertrages": (
                f"Regelmäßige Wartung der {d['type']} {d['manufacturer']} {d['model']}"
                f" im Objekt {building['address']}."
            ),
            "Vereinbarungen_Leistungen": [
                f"Inspektion und Wartung der {d['type']} gemäß Herstellervorgaben und einschlägigen Normen",
                "Reinigung, Funktionsprüfung und Dokumentation aller sicherheitsrelevanten Bauteile",
            ],
            "Wartungsintervall": c["frequency"],
            "Laufzeit": {
                "Startdatum": c["start"],
                "Enddatum": c["end"],
                "Kuendigungsfrist": {
                    "Frist": "3 Monate",
                    "Zum": "Vertragsende",
                },
            },
            "Kosten": {
                "Betrag": c["cost"],
                "Waehrung": "EUR",
                "Bezugseinheit": "Jahr" if c["frequency"] == "Jährlich" else "Halbjahr",
            },
            "Gerichtsstand": building["city"],
            "Unterschriften": [
                {
                    "Rolle": "Auftraggeber",
                    "Unterschrift_von": unit["unit_contact"],
                    "Ort": unit["unit_sign_city"],
                    "Datum": c["sign_date"],
                },
                {
                    "Rolle": "Auftragnehmer",
                    "Unterschrift_von": c["provider_technician"],
                    "Ort": c["provider_city"],
                    "Datum": c["sign_date"],
                },
            ],
        },
        "optional": {
            "Reaktionszeit_bei_Stoerung": "Innerhalb von 8 Stunden an Werktagen (Mo–Fr, 07:00–17:00 Uhr)",
            "Zusatzleistungen": [
                "Notfalldienst außerhalb der regulären Arbeitszeiten auf Anfrage",
                "Erstellung eines Wartungsberichts nach jeder Wartung",
            ],
            "Zahlungsbedingungen": "Zahlung innerhalb von 14 Tagen nach Rechnungsstellung ohne Abzug",
            "Haftungsklauseln": (
                "Der Auftragnehmer haftet nur für Schäden durch nachgewiesene Fahrlässigkeit."
                " Die Haftung ist auf die jährliche Wartungsvergütung begrenzt."
            ),
            "Gewaehrleistungszeit": "12 Monate auf durchgeführte Wartungsleistungen und eingebaute Ersatzteile",
            "Preisanpassungsklausel": "Jährliche Anpassung um maximal 3 % mit Ankündigungsfrist von 6 Wochen",
            "Mehrwertsteuer": "19 %",
        },
    }


def _make_protocol(
    unit: dict, building: dict, device: dict, contract: dict, proto: dict
) -> dict:
    c = contract
    d = device
    p = proto
    return {
        "meta": {
            "entity": "MaintenanceProtocol",
            "field_values": {
                "id": None,
                "contract_id": c["id"],
                "device_id": None,
                "device_type": d["type"],
                "maintenance_date": p["date"],
                "maintenance_type": None,
                "performed_by_id": None,
                "ordered_by_id": None,
                "result_deficiency": p["result"],
                "deficiency_type": None,
            },
        },
        "required": {
            "Anlagentyp": {
                "Typ": d["type"],
                "Hersteller": d["manufacturer"],
                "Modell": d["model"],
                "Seriennummer": d["serial"],
                "Anzahl": "1",
            },
            "Anlagenstandort": {
                "Adresse": building["address"],
                "Objekttyp": building["type"],
            },
            "Datum_der_Wartung": p["date"],
            "Durchgefuehrte_Arbeiten": [
                {
                    "Arbeitspunkt": f"Inspektion und Wartung der {d['type']} gemäß Wartungsvertrag {c['id']}",
                    "Ergebnis": p["result"],
                },
                {
                    "Arbeitspunkt": "Überprüfung aller sicherheitsrelevanten Bauteile und Dokumentation",
                    "Ergebnis": "Alle geprüften Komponenten in ordnungsgemäßem Zustand",
                },
            ],
            "Bemerkungen": p["remarks"],
            "Wartungsergebnis": p["result"],
            "Ausfuehrende_Fachfirma": {
                "Firma": c["provider"],
                "KD_Techniker": c["provider_technician"],
                "Strasse": c["provider_addr"].split(",")[0],
                "PLZ": c["provider_addr"].split(",")[1].strip().split(" ")[0]
                if "," in c["provider_addr"]
                else "",
                "Ort": c["provider_city"],
                "Tel": c["provider_phone"],
                "E_Mail": c["provider_email"],
            },
            "Unterschriften": [
                {
                    "Rolle": "Ausführender Techniker",
                    "Unterschrift_von": c["provider_technician"],
                    "Datum": p["date"],
                },
                {
                    "Rolle": "Auftraggeber / Gebäudeverantwortlicher",
                    "Unterschrift_von": unit["unit_contact"],
                    "Datum": p["date"],
                },
            ],
        },
        "optional": {
            "Auftraggeber": {
                "Name": unit["unit_name"],
                "Anschrift": building["address"],
            },
            "Naechster_Wartungstermin": None,
            "Datum_Inbetriebnahme": None,
            "Verwendete_Ersatzteile": [],
            "Messwerte": [],
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main generation
# ─────────────────────────────────────────────────────────────────────────────


def generate() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    contract_files: list[Path] = []
    protocol_files: list[Path] = []
    contract_idx = 1
    protocol_idx = 1

    for unit in SCENARIO:
        for building in unit["buildings"]:
            for device in building["devices"]:
                for contract in device["contracts"]:
                    # ── Write contract ────────────────────────────────────
                    c_data = _make_contract(unit, building, device, contract)
                    c_name = f"MaintenanceContract_{contract_idx:02d}.json"
                    c_path = OUT / c_name
                    c_path.write_text(
                        json.dumps(c_data, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )
                    contract_files.append(c_path)
                    print(f"  Wrote {c_name}")
                    contract_idx += 1

                    # ── Write protocols ───────────────────────────────────
                    for proto in contract["protocols"]:
                        p_data = _make_protocol(unit, building, device, contract, proto)
                        p_name = f"MaintenanceProtocol_{protocol_idx:02d}.json"
                        p_path = OUT / p_name
                        p_path.write_text(
                            json.dumps(p_data, indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )
                        protocol_files.append(p_path)
                        print(f"  Wrote {p_name}")
                        protocol_idx += 1

    # ── Generate ontology.json ────────────────────────────────────────────────
    sys.path.insert(0, str(BASE))
    from ontology_view import build_ontology

    all_files = contract_files + protocol_files
    ontology = build_ontology(all_files)
    ont_path = OUT / "ontology.json"
    ont_path.write_text(
        json.dumps(ontology, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Wrote ontology.json")

    s = ontology["summary"]
    print(
        f"\nDone — {s['economic_units']} units, {s['buildings']} buildings,"
        f" {s['contracts']} contracts, {s['protocols']} protocols"
    )
    print(f"Output: {OUT}")


if __name__ == "__main__":
    generate()
