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
}


@dataclass
class DocumentType:
    name: str
    requirements_file: str
    few_shot_files: list[str]

    def requirements_file_for(self, system_key: str) -> str:
        doc_dir = self.requirements_file.replace(".txt", "")
        per_system = f"{doc_dir}/{system_key}.txt"
        if (Path(__file__).parent / per_system).exists():
            return per_system
        return self.requirements_file


REAL_ESTATE_TAXONOMY: dict[str, DocumentType] = {
    "wartungsprotokoll": DocumentType(
        name="Wartungsprotokoll",
        requirements_file="document_requirements/wartungsprotokoll.txt",
        few_shot_files=[
            "few_shots/Wartungsprotokoll_Waermepumpe-1.pdf",
            "few_shots/Wartungsprotokoll-Rauchwarnmelder-2.pdf",
        ],
    ),
    "wartungsvertrag": DocumentType(
        name="Wartungsvertrag",
        requirements_file="document_requirements/wartungsvertrag.txt",
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
