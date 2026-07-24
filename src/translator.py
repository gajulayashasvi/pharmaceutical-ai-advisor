"""Translator - Translate medical content to multiple languages"""

from typing import Dict

class Translator:
    """Translate medical information to multiple languages"""
    
    def __init__(self):
        self.translations = {
            "English": {
                "Disease": "Disease",
                "Medicine": "Medicine",
                "Symptom": "Symptom",
                "Dosage": "Dosage",
                "Side Effects": "Side Effects",
                "Price": "Price",
            },
            "Hindi": {
                "Disease": "रोग",
                "Medicine": "दवा",
                "Symptom": "लक्षण",
                "Dosage": "खुराक",
                "Side Effects": "दुष्प्रभाव",
                "Price": "कीमत",
            },
            "Spanish": {
                "Disease": "Enfermedad",
                "Medicine": "Medicamento",
                "Symptom": "Síntoma",
                "Dosage": "Dosis",
                "Side Effects": "Efectos secundarios",
                "Price": "Precio",
            },
            "French": {
                "Disease": "Maladie",
                "Medicine": "Médicament",
                "Symptom": "Symptôme",
                "Dosage": "Dosage",
                "Side Effects": "Effets secondaires",
                "Price": "Prix",
            },
        }
    
    def translate(self, text: str, language: str) -> str:
        """Translate text to specified language"""
        if language == "English":
            return text
        
        # Simple word-by-word translation
        translated = text
        for key, value in self.translations.get(language, {}).items():
            translated = translated.replace(key, value)
        
        return translated
