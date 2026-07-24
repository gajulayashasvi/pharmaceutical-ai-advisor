"""Search Utils - Utility functions for searching medicines and diseases"""

from typing import List, Dict

class SearchUtils:
    """Utility functions for searching medicines and diseases"""
    
    def __init__(self, medicines_db: List[Dict], diseases_db: List[Dict]):
        self.medicines_db = medicines_db
        self.diseases_db = diseases_db
    
    def search_medicines(self, query: str) -> List[Dict]:
        """Search medicines by name or use"""
        query_lower = query.lower()
        results = []
        
        for medicine in self.medicines_db:
            # Search by name
            if query_lower in medicine['name'].lower():
                results.append(medicine)
            # Search by uses
            elif any(query_lower in use.lower() for use in medicine.get('uses', [])):
                results.append(medicine)
        
        return results
    
    def search_diseases(self, query: str) -> List[Dict]:
        """Search diseases by name or symptoms"""
        query_lower = query.lower()
        results = []
        
        for disease in self.diseases_db:
            # Search by name
            if query_lower in disease['name'].lower():
                results.append(disease)
            # Search by symptoms
            elif any(query_lower in symptom.lower() for symptom in disease.get('symptoms', [])):
                results.append(disease)
        
        return results
    
    def filter_by_price(self, medicines: List[Dict], max_price: float) -> List[Dict]:
        """Filter medicines by maximum price"""
        return [med for med in medicines if med.get('price', float('inf')) <= max_price]
    
    def filter_by_availability(self, medicines: List[Dict], availability: str) -> List[Dict]:
        """Filter medicines by availability"""
        return [med for med in medicines if med.get('availability', '').lower() == availability.lower()]
    
    def sort_by_price(self, medicines: List[Dict], ascending: bool = True) -> List[Dict]:
        """Sort medicines by price"""
        return sorted(medicines, key=lambda x: x.get('price', float('inf')), reverse=not ascending)
    
    def get_medicine_details(self, medicine_name: str) -> Dict:
        """Get detailed information about a medicine"""
        medicine_name_lower = medicine_name.lower()
        for medicine in self.medicines_db:
            if medicine['name'].lower() == medicine_name_lower:
                return medicine
        return {}
    
    def get_disease_details(self, disease_name: str) -> Dict:
        """Get detailed information about a disease"""
        disease_name_lower = disease_name.lower()
        for disease in self.diseases_db:
            if disease['name'].lower() == disease_name_lower:
                return disease
        return {}
