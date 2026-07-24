"""Medicine Matcher - Match diseases to appropriate medicines"""

from typing import List, Dict

class MedicineMatcher:
    """Match diseases to appropriate medicines based on symptoms and conditions"""
    
    def __init__(self, medicines_db: List[Dict], diseases_db: List[Dict]):
        self.medicines_db = medicines_db
        self.diseases_db = diseases_db
    
    def find_medicines_for_disease(self, disease_name: str) -> List[Dict]:
        """Find medicines recommended for a specific disease"""
        disease = self._find_disease(disease_name)
        
        if not disease:
            return []
        
        medicines = []
        for med_name in disease.get('recommended_medicines', []):
            medicine = self._find_medicine(med_name)
            if medicine:
                medicines.append(medicine)
        
        return medicines
    
    def find_diseases_by_symptoms(self, symptoms: List[str]) -> List[Dict]:
        """Find diseases that match given symptoms"""
        matching_diseases = []
        
        for disease in self.diseases_db:
            disease_symptoms = [s.lower() for s in disease.get('symptoms', [])]
            matching_count = 0
            
            for symptom in symptoms:
                symptom_normalized = symptom.replace('_', ' ').lower()
                if any(symptom_normalized in ds for ds in disease_symptoms):
                    matching_count += 1
            
            if matching_count > 0:
                match_score = (matching_count / len(symptoms)) * 100 if symptoms else 0
                disease_copy = disease.copy()
                disease_copy['match_score'] = round(match_score, 1)
                disease_copy['matching_symptoms'] = symptoms[:matching_count]
                matching_diseases.append(disease_copy)
        
        matching_diseases.sort(key=lambda x: x['match_score'], reverse=True)
        return matching_diseases
    
    def _find_disease(self, disease_name: str) -> Dict:
        """Find a disease by name (case-insensitive)"""
        disease_name_lower = disease_name.lower()
        for disease in self.diseases_db:
            if disease['name'].lower() == disease_name_lower:
                return disease
        return None
    
    def _find_medicine(self, medicine_name: str) -> Dict:
        """Find a medicine by name (case-insensitive)"""
        medicine_name_lower = medicine_name.lower()
        for medicine in self.medicines_db:
            if medicine['name'].lower() == medicine_name_lower:
                return medicine
        return None
