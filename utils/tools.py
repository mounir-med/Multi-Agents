import math
from typing import Dict, Any

def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
    """Calcule l'Indice de Masse Corporelle (IMC)."""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    category = ""
    if bmi < 18.5: category = "Insuffisance pondérale"
    elif bmi < 25: category = "Poids normal"
    elif bmi < 30: category = "Surpoids"
    else: category = "Obésité"
    
    return {
        "bmi": round(bmi, 2),
        "category": category,
        "advice": "Ces résultats sont indicatifs. Consultez un professionnel de santé."
    }

def drug_interaction_check(drugs: list[str]) -> str:
    """Mock d'une vérification d'interaction médicamenteuse."""
    interactions = {
        ("aspirine", "warfarine"): "Risque accru de saignement. Surveillance requise.",
        ("ibuprofène", "aspirine"): "L'ibuprofène peut réduire l'effet antiplaquettaire de l'aspirine.",
        ("amoxicilline", "méthotrexate"): "Risque de toxicité du méthotrexate."
    }
    
    found = []
    drugs_lower = [d.lower() for d in drugs]
    for (d1, d2), msg in interactions.items():
        if d1 in drugs_lower and d2 in drugs_lower:
            found.append(f"Interaction {d1}/{d2} : {msg}")
            
    if not found:
        return "Aucune interaction majeure détectée entre ces substances (base de données limitée)."
    return "\n".join(found)

MEDICAL_TOOLS = [
    {
        "name": "calculate_bmi",
        "description": "Calcule l'IMC à partir du poids (kg) et de la taille (cm)",
        "func": calculate_bmi
    },
    {
        "name": "drug_interaction_check",
        "description": "Vérifie les interactions entre une liste de médicaments",
        "func": drug_interaction_check
    }
]
