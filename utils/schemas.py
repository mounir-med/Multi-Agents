from pydantic import BaseModel, Field
from typing import List, Optional

class Citation(BaseModel):
    text: str = Field(..., description="Le texte exact cité de la source")
    source: str = Field(..., description="Le nom ou l'identifiant de la source")

class AnalysisResponse(BaseModel):
    key_findings: List[str] = Field(..., description="Liste des découvertes principales")
    severity: str = Field(..., description="Niveau de sévérité (Normal, Attention, Critique)")
    suggested_diagnoses: List[str] = Field(..., description="Diagnostics suggérés basés sur le contexte")
    detailed_analysis: str = Field(..., description="Analyse détaillée complète")

class MedicalReport(BaseModel):
    summary: str = Field(..., description="Résumé succinct du cas")
    symptoms: List[str] = Field(..., description="Liste des symptômes identifiés")
    clinical_analysis: str = Field(..., description="Analyse clinique approfondie")
    recommendations: List[str] = Field(..., description="Recommandations médicales")
    citations: List[Citation] = Field(..., description="Citations textuelles précises des sources")

class ValidationAudit(BaseModel):
    is_valid: bool = Field(..., description="Si le rapport est valide et sans hallucinations")
    corrections_needed: Optional[str] = Field(None, description="Description des corrections nécessaires si non valide")
    confidence_score: float = Field(..., description="Score de confiance de 0 à 1")
