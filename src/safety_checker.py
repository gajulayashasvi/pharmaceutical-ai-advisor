"""Safety Checker - Check for drug interactions and contraindications"""

from typing import List, Dict

class SafetyChecker:
    """Check for drug interactions, contraindications, and safety issues"""
    
    def __init__(self, medicines_db: List[Dict]):
        self.medicines_db = medicines_db
    
    def check_interactions(self, medicines: List[str], additional_meds: List[str] = None) -> List[str]:
        """Check for interactions between multiple medicines"""
        all_medicines = medicines + (additional_meds or [])
        warnings = []
        
        for i, med1_name in enumerate(medicines):
            medicine1 = self._find_medicine(med1_name)
            if not medicine1:
                continue
            
            # Check against other selected medicines
            for med2_name in all_medicines[i+1:]:
                medicine2 = self._find_medicine(med2_name)
                if not medicine2:
                    continue
                
                # Check for interactions
                interactions = medicine1.get('interactions', [])
                for interaction in interactions:
                    if med2_name.lower() in interaction.lower() or medicine2['name'].lower() in interaction.lower():
                        warnings.append(f"⚠️ INTERACTION WARNING: {medicine1['name']} may interact with {medicine2['name']}")
        
        return warnings
    
    def check_contraindications(self, medicines: List[str], health_conditions: List[str]) -> List[str]:
        """Check if medicines are contraindicated for given health conditions"""
        warnings = []
        
        for med_name in medicines:
            medicine = self._find_medicine(med_name)
            if not medicine:
                continue
            
            contraindications = medicine.get('contraindications', [])
            for condition in health_conditions:
                for contraindication in contraindications:
                    if condition.lower() in contraindication.lower():
                        warnings.append(f"🚫 CONTRAINDICATION: {medicine['name']} is contraindicated for {condition}")
        
        return warnings
    
    def check_side_effects(self, medicine_name: str) -> List[str]:
        """Get side effects for a medicine"""
        medicine = self._find_medicine(medicine_name)
        if medicine:
            return medicine.get('side_effects', [])
        return []
    
    def check_precautions(self, medicine_name: str) -> str:
        """Get precautions for a medicine"""
        medicine = self._find_medicine(medicine_name)
        if medicine:
            return medicine.get('precautions', 'Consult a healthcare professional')
        return 'Medicine not found'
    
    def _find_medicine(self, medicine_name: str) -> Dict:
        """Find a medicine by name (case-insensitive)"""
        medicine_name_lower = medicine_name.lower()
        for medicine in self.medicines_db:
            if medicine['name'].lower() == medicine_name_lower:
                return medicine
        return None
