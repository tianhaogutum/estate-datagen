"""
Maintenance Document Taxonomy
"""

from dataclasses import dataclass
from pathlib import Path

SYSTEM_TYPES: dict[str, str] = {
    "KLIMAANLAGE": "Klimaanlage",
    "WAERMEPUMPE": "Wärmepumpe",
    "HEIZKESSEL": "Heizkessel",
    "LUEFTUNGSANLAGE": "Lüftungsanlage",
    "BRANDMELDEANLAGE": "Brandmeldeanlage",
    "SPRINKLER": "Sprinkleranlage",
    "RAUCHMELDER": "Rauchwarnmelder",
    "FEUERSCHUTZTUER": "Feuerschutztür",
    "RAUCHSCHUTZ_RWA": "Rauch- und Wärmeabzugsanlage",
    "SICHERHEITSBELEUCHTUNG": "Sicherheitsbeleuchtung",
    "AUFZUG_PERSONEN": "Personenaufzug",
    "ELEKTRISCHE_ANLAGE": "Elektrische Anlage",
    "HEBEANLAGE_ABWASSER": "Hebeanlage Abwasser",
    "NOTSTROMAGGREGAT": "Notstromaggregat",
    "FEUERSCHUTZABSCHLUSS": "Rauch- und Feuerschutzabschluss",
    "FEUERSCHUTZEINRICHTUNG_MANUELL": "Wandhydrant / Handfeuerlöscher",
    "SANITAER_ALLG": "Sanitärtechnik allgemein",
    "ELEKTRISCHE_ANLAGE_MOBIL": "Nichtortsfeste elektrische Betriebsmittel",
    "BLITZSCHUTZ": "Blitzschutzanlage",
    "DRUCKBEHAELTER": "Druckbehälter / Druckanlage",
    "CO_WARNANLAGE": "CO-Warnanlage",
}


@dataclass
class DocumentType:
    name: str
    doc_key: str
    few_shot_files: list[str]

    def requirements_file_for(self, system_key: str) -> str:
        per_system = f"document_requirements/{self.doc_key}/{system_key}.txt"
        if not (Path(__file__).parent / per_system).exists():
            raise FileNotFoundError(
                f"No requirements file for '{self.name}' / '{system_key}': {per_system}"
            )
        return per_system


REAL_ESTATE_TAXONOMY: dict[str, DocumentType] = {
    "wartungsprotokoll": DocumentType(
        name="Wartungsprotokoll",
        doc_key="wartungsprotokoll",
        few_shot_files=[
            "few_shots/Wartungsprotokoll_Waermepumpe-1.pdf",
            "few_shots/Wartungsprotokoll-Rauchwarnmelder-2.pdf",
        ],
    ),
    "wartungsvertrag": DocumentType(
        name="Wartungsvertrag",
        doc_key="wartungsvertrag",
        few_shot_files=[
            "few_shots/Wartungsvertrag-Wärmepumpe-1.pdf",
            "few_shots/Wartungsvertrag_für_Rauchwarnmelder-2.pdf",
        ],
    ),
}


def get_document(doc_key: str) -> DocumentType:
    if doc_key not in REAL_ESTATE_TAXONOMY:
        raise KeyError(
            f"Unknown document type: {doc_key}. Options: {list(REAL_ESTATE_TAXONOMY)}"
        )
    return REAL_ESTATE_TAXONOMY[doc_key]


def get_system_name(system_key: str) -> str:
    if system_key not in SYSTEM_TYPES:
        raise KeyError(
            f"Unknown system type: {system_key}. Options: {list(SYSTEM_TYPES)}"
        )
    return SYSTEM_TYPES[system_key]


if __name__ == "__main__":
    for doc_key, doc in REAL_ESTATE_TAXONOMY.items():
        print(f"{doc_key}: {doc.name}")
    print(f"\nSystem types ({len(SYSTEM_TYPES)}): {', '.join(SYSTEM_TYPES)}")
