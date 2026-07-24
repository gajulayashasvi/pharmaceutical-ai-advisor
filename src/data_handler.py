"""Data Handler - Load and manage pharmaceutical data"""

import json
from typing import List, Dict

class DataHandler:
    """Handle loading and managing pharmaceutical data"""
    
    def __init__(self):
        self.medicines_db = []
        self.diseases_db = []
    
    def load_medicines_data(self, file_path: str) -> List[Dict]:
        """Load medicines data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                self.medicines_db = json.load(f)
            return self.medicines_db
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return []
    
    def load_diseases_data(self, file_path: str) -> List[Dict]:
        """Load diseases data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                self.diseases_db = json.load(f)
            return self.diseases_db
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return []
    
    def get_all_medicines(self) -> List[Dict]:
        """Get all medicines"""
        return self.medicines_db
    
    def get_all_diseases(self) -> List[Dict]:
        """Get all diseases"""
        return self.diseases_db
    
    def add_medicine(self, medicine: Dict) -> bool:
        """Add a new medicine to the database"""
        if 'name' in medicine:
            self.medicines_db.append(medicine)
            return True
        return False
    
    def add_disease(self, disease: Dict) -> bool:
        """Add a new disease to the database"""
        if 'name' in disease:
            self.diseases_db.append(disease)
            return True
        return False
    
    def save_medicines_data(self, file_path: str) -> bool:
        """Save medicines data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.medicines_db, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving medicines data: {e}")
            return False
    
    def save_diseases_data(self, file_path: str) -> bool:
        """Save diseases data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.diseases_db, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving diseases data: {e}")
            return False
    
    def get_medicine_count(self) -> int:
        """Get total number of medicines"""
        return len(self.medicines_db)
    
    def get_disease_count(self) -> int:
        """Get total number of diseases"""
        return len(self.diseases_db)
