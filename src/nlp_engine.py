"""NLP Engine for symptom extraction and medical text processing"""

import re
from typing import List, Dict

class SymptomExtractor:
    """Extract symptoms from natural language text using pattern matching and keyword extraction"""
    
    def __init__(self):
        self.symptom_keywords = {
            "headache": ["head pain", "headache", "head ache", "migraine", "throbbing head", "pressure in head"],
            "fever": ["fever", "high temperature", "chills", "body heat", "feverish", "high temp"],
            "cold": ["cold", "flu", "cough", "sneeze", "runny nose", "congestion", "nasal"],
            "cough": ["cough", "coughing", "throat irritation", "dry cough", "wet cough"],
            "stomach_pain": ["stomach ache", "belly pain", "abdominal pain", "stomach cramps", "gastric"],
            "joint_pain": ["joint pain", "arthritis", "knee pain", "back pain", "muscle pain", "bone pain"],
            "nausea": ["nausea", "feeling sick", "vomiting", "throwing up", "queasy"],
            "diarrhea": ["diarrhea", "loose motion", "loose stools", "bowel"],
            "constipation": ["constipation", "hard stools", "difficulty bowel"],
            "rash": ["rash", "skin rash", "itching", "itch", "skin irritation", "hives"],
            "sore_throat": ["sore throat", "throat pain", "throat ache", "pharyngitis"],
            "dizziness": ["dizziness", "dizzy", "vertigo", "lightheaded", "spinning head"],
            "fatigue": ["fatigue", "tired", "tiredness", "weakness", "exhaustion", "weak"],
            "anxiety": ["anxiety", "anxious", "nervous", "panic attack", "worry"],
            "depression": ["depression", "depressed", "sad", "sadness", "unhappy"],
        }
    
    def extract_symptoms(self, user_input: str) -> List[str]:
        """Extract symptoms from user input"""
        detected_symptoms = []
        user_input_lower = user_input.lower()
        
        for symptom, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    detected_symptoms.append(symptom)
                    break
        
        return list(set(detected_symptoms))
    
    def extract_severity(self, text: str) -> str:
        """Extract severity of symptoms"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["severe", "critical", "very", "extremely"]):
            return "severe"
        elif any(word in text_lower for word in ["moderate", "medium"]):
            return "moderate"
        else:
            return "mild"
