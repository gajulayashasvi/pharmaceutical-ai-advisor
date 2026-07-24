"""Disease Finder - Find diseases that a medicine treats"""

from typing import List, Dict

class DiseaseFinder:
    """Find diseases that can be treated with a specific medicine"""
    
    def __init__(self, medicines_db: List[Dict], diseases_db: List[Dict]):
        self.medicines_db = medicines_db
        self.diseases_db = diseases_db
    
    def find_diseases_for_medicine(self, medicine_name: str) -> List[Dict]:
        """Find diseases that can be treated with a specific medicine"""
        medicine = self._find_medicine(medicine_name)
        
        if not medicine:
            return []
        
        diseases = []
        medicine_uses = medicine.get('uses', [])
        
        for disease in self.diseases_db:
            for use in medicine_uses:
                if use.lower() in [s.lower() for s in disease.get('symptoms', [])]:
                    diseases.append(disease)
                    break
        
        return diseases
    
    def find_medicines_by_use(self, use: str) -> List[Dict]:
        """Find all medicines for a specific use"""
        use_lower = use.lower()
        medicines = []
        
        for medicine in self.medicines_db:
            for med_use in medicine.get('uses', []):
                if use_lower in med_use.lower():
                    medicines.append(medicine)
                    break
        
        return medicines
    
    def _find_medicine(self, medicine_name: str) -> Dict:
        """Find a medicine by name (case-insensitive)"""
        medicine_name_lower = medicine_name.lower()
        for medicine in self.medicines_db:
            if medicine['name'].lower() == medicine_name_lower:
                return medicine
        return None
