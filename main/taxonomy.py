"""
Maintenance Document Taxonomy

Defines the taxonomy for maintenance-related real estate documents:
- Wartungsprotokoll (Maintenance Protocol)
- Wartungsvertrag  (Maintenance Contract)

Each document type lists the required and optional fields and the files that
describe and exemplify it.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class DocumentCategory(Enum):
    MAINTENANCE = "Maintenance"


@dataclass
class DocumentType:
    name: str
    category: DocumentCategory
    description: str
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    requirements_file: str = ""
    few_shot_files: list[str] = field(default_factory=list)


REAL_ESTATE_TAXONOMY: dict[str, DocumentType] = {
    "wartungsprotokoll": DocumentType(
        name="Wartungsprotokoll",
        category=DocumentCategory.MAINTENANCE,
        description="Protocol documenting a performed maintenance visit on a building system.",
        required_fields=[
            "Anlagentyp",
            "Anlagenstandort",
            "Datum der Wartung",
            "Durchgeführte Arbeiten",
            "Bemerkungen",
            "Wartungsergebnis",
            "Unterschriften",
        ],
        optional_fields=[
            "Auftraggeber",
            "Ausfuehrende_Fachfirma",
            "Naechster_Wartungstermin",
            "Datum_Inbetriebnahme",
            "Verwendete_Ersatzteile",
            "Messwerte",
            "Historie",
            "Pruefberichte_pro_Raum",
            "Kaeltetechnische_Pruefung",
        ],
        requirements_file="document_requirements/wartungsprotokoll.txt",
        few_shot_files=[
            "few_shots/Wartungsprotokoll_Waermepumpe-1.pdf",
            "few_shots/Wartungsprotokoll-Rauchwarnmelder-2.pdf",
        ],
    ),
    "wartungsvertrag": DocumentType(
        name="Wartungsvertrag",
        category=DocumentCategory.MAINTENANCE,
        description="Contract between a customer and a contractor defining maintenance services for a system.",
        required_fields=[
            "Anlagentyp",
            "Auftraggeber",
            "Auftragnehmer",
            "Objekt der Wartung",
            "Gegenstand_des_Vertrages",
            "Vereinbarungen",
            "Wartungsintervall",
            "Laufzeit",
            "Kosten",
            "Gerichtsstand",
            "Unterschriften",
        ],
        optional_fields=[
            "Reaktionszeit_bei_Stoerung",
            "Zusatzleistungen",
            "Zahlungsbedingungen",
            "Haftungsklauseln",
            "Gewaehrleistungszeit",
            "Preisanpassungsklausel",
            "Mehrwertsteuer",
            "Anlagen_Stueckzahl",
        ],
        requirements_file="document_requirements/wartungsvertrag.txt",
        few_shot_files=[
            "few_shots/Wartungsvertrag-Wärmepumpe-1.pdf",
            "few_shots/Wartungsvertrag_für_Rauchwarnmelder-2.pdf",
        ],
    ),
}


def list_categories() -> list[str]:
    return [c.value for c in DocumentCategory]


def list_documents_by_category(category: DocumentCategory) -> list[DocumentType]:
    return [doc for doc in REAL_ESTATE_TAXONOMY.values() if doc.category == category]


def get_document(doc_key: str) -> DocumentType:
    if doc_key not in REAL_ESTATE_TAXONOMY:
        raise KeyError(f"Unknown document type: {doc_key}")
    return REAL_ESTATE_TAXONOMY[doc_key]


def print_taxonomy() -> None:
    base = Path(__file__).parent
    for category in DocumentCategory:
        print(f"\n[{category.value}]")
        for doc in list_documents_by_category(category):
            print(f"  - {doc.name}")
            print(f"      description: {doc.description}")
            print(
                f"      required fields ({len(doc.required_fields)}): {', '.join(doc.required_fields)}"
            )
            print(
                f"      optional fields ({len(doc.optional_fields)}): {', '.join(doc.optional_fields)}"
            )
            print(f"      requirements file: {base / doc.requirements_file}")


if __name__ == "__main__":
    print_taxonomy()
