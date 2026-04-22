"""
Maintenance Document Taxonomy

Defines the taxonomy for maintenance-related real estate documents:
- Wartungsprotokoll (Maintenance Protocol)
- Wartungsvertrag  (Maintenance Contract)

Each document type lists the required and optional fields and the files that
describe and exemplify it. Documents are further specialized by system type
(e.g. WAERMEPUMPE, BRANDMELDEANLAGE).
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# -------------------------
# System types
# -------------------------


class SystemCategory(Enum):
    HVAC_ENERGY = "暖通与能源"
    SAFETY_FIRE = "安全与消防"
    INFRASTRUCTURE = "基础设施"


@dataclass
class SystemType:
    key: str
    german_name: str
    category: SystemCategory


SYSTEM_TYPES: dict[str, SystemType] = {
    "KLIMAANLAGE": SystemType("KLIMAANLAGE", "Klimaanlage", SystemCategory.HVAC_ENERGY),
    "WAERMEPUMPE": SystemType("WAERMEPUMPE", "Wärmepumpe", SystemCategory.HVAC_ENERGY),
    "HEIZKESSEL": SystemType("HEIZKESSEL", "Heizkessel", SystemCategory.HVAC_ENERGY),
    "LUEFTUNGSANLAGE": SystemType(
        "LUEFTUNGSANLAGE", "Lüftungsanlage", SystemCategory.HVAC_ENERGY
    ),
    "BRANDMELDEANLAGE": SystemType(
        "BRANDMELDEANLAGE", "Brandmeldeanlage", SystemCategory.SAFETY_FIRE
    ),
    "SPRINKLER": SystemType("SPRINKLER", "Sprinkleranlage", SystemCategory.SAFETY_FIRE),
    "RAUCHMELDER": SystemType(
        "RAUCHMELDER", "Rauchwarnmelder", SystemCategory.SAFETY_FIRE
    ),
    "FEUERSCHUTZTUER": SystemType(
        "FEUERSCHUTZTUER", "Feuerschutztür", SystemCategory.SAFETY_FIRE
    ),
    "RAUCHSCHUTZ_RWA": SystemType(
        "RAUCHSCHUTZ_RWA", "Rauch- und Wärmeabzugsanlage", SystemCategory.SAFETY_FIRE
    ),
    "SICHERHEITSBELEUCHTUNG": SystemType(
        "SICHERHEITSBELEUCHTUNG", "Sicherheitsbeleuchtung", SystemCategory.SAFETY_FIRE
    ),
    "AUFZUG_PERSONEN": SystemType(
        "AUFZUG_PERSONEN", "Personenaufzug", SystemCategory.INFRASTRUCTURE
    ),
    "ELEKTRISCHE_ANLAGE": SystemType(
        "ELEKTRISCHE_ANLAGE", "Elektrische Anlage", SystemCategory.INFRASTRUCTURE
    ),
    "HEBEANLAGE_ABWASSER": SystemType(
        "HEBEANLAGE_ABWASSER", "Hebeanlage Abwasser", SystemCategory.INFRASTRUCTURE
    ),
    "NOTSTROMAGGREGAT": SystemType(
        "NOTSTROMAGGREGAT", "Notstromaggregat", SystemCategory.INFRASTRUCTURE
    ),
}


def list_system_types_by_category(category: SystemCategory) -> list[SystemType]:
    return [s for s in SYSTEM_TYPES.values() if s.category == category]


def get_system_type(key: str) -> SystemType:
    if key not in SYSTEM_TYPES:
        raise KeyError(f"Unknown system type: {key}. Options: {list(SYSTEM_TYPES)}")
    return SYSTEM_TYPES[key]


# -------------------------
# Document types
# -------------------------


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
    system_types: list[str] = field(default_factory=lambda: list(SYSTEM_TYPES.keys()))

    def requirements_file_for(self, system_key: str) -> str:
        """Return the per-system requirements file path, falling back to the generic one."""
        doc_dir = self.requirements_file.replace(".txt", "")
        per_system = f"{doc_dir}/{system_key}.txt"
        base = Path(__file__).parent
        if (base / per_system).exists():
            return per_system
        return self.requirements_file


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


# -------------------------
# Helpers
# -------------------------


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
            print(f"      system types ({len(doc.system_types)}):")
            for cat in SystemCategory:
                systems = [
                    SYSTEM_TYPES[k].german_name
                    for k in doc.system_types
                    if SYSTEM_TYPES[k].category == cat
                ]
                if systems:
                    print(f"        [{cat.value}] {', '.join(systems)}")


if __name__ == "__main__":
    print_taxonomy()
