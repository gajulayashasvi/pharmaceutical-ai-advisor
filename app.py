import streamlit as st
import json
import os
from datetime import datetime
from src.nlp_engine import SymptomExtractor
from src.medicine_matcher import MedicineMatcher
from src.disease_finder import DiseaseFinder
from src.safety_checker import SafetyChecker
from utils.search_utils import fuzzy_search
from utils.data_loader import load_medicines, load_diseases

# Page configuration
st.set_page_config(
    page_title="Pharmaceutical AI Advisor",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3em;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .subheader {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ff9800;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'medical_history' not in st.session_state:
    st.session_state.medical_history = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Load data
@st.cache_resource
def load_all_data():
    medicines = load_medicines()
    diseases = load_diseases()
    return medicines, diseases

medicines_db, diseases_db = load_all_data()

# Initialize components
@st.cache_resource
def initialize_components():
    extractor = SymptomExtractor()
    matcher = MedicineMatcher(medicines_db, diseases_db)
    disease_finder = DiseaseFinder(medicines_db, diseases_db)
    checker = SafetyChecker(medicines_db)
    return extractor, matcher, disease_finder, checker

extractor, matcher, disease_finder, checker = initialize_components()

# Main header
st.markdown('<div class="main-header">💊 Pharmaceutical AI Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Your Intelligent Medicine & Disease Guide</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("⚙️ Configuration")
    
    language = st.selectbox(
        "Select Language:",
        ["English", "Hindi", "Spanish", "French"],
        key="language_selector"
    )
    
    st.markdown("---")
    st.subheader("👤 Your Medical Profile")
    
    existing_conditions = st.multiselect(
        "Your Health Conditions:",
        [
            "Diabetes", "Heart Disease", "Hypertension", "Asthma",
            "Liver Disease", "Kidney Disease", "Thyroid Disease",
            "Arthritis", "Obesity", "Anxiety", "Depression", "Epilepsy",
            "Migraine", "COPD", "Anemia", "Autoimmune Disease"
        ],
        key="conditions_selector"
    )
    
    current_medications = st.multiselect(
        "Current Medications:",
        [med['name'] for med in medicines_db] if medicines_db else [],
        key="medications_selector"
    )
    
    if existing_conditions or current_medications:
        st.success("Profile updated ✓")
    
    st.markdown("---")
    st.subheader("📊 Quick Info")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Medicines", len(medicines_db))
    with col2:
        st.metric("Diseases", len(diseases_db))
    
    st.markdown("---")
    st.markdown("⚠️ **DISCLAIMER**")
    st.markdown("""
    This app is for **educational purposes only**. 
    
    - NOT a substitute for medical advice
    - Always consult a healthcare professional
    - In emergencies, call emergency services
    - Information may be incomplete
    """)

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Search by Disease",
    "💊 Search by Medicine",
    "📚 Disease Knowledge Base",
    "🩺 Symptom Checker",
    "⚠️ Interaction Checker",
    "📖 Medicine Directory"
])

# TAB 1: Search by Disease
with tab1:
    st.header("🔍 Search by Disease")
    st.write("Enter a disease name to find recommended medicines, symptoms, and treatment information.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        disease_search = st.text_input(
            "Enter disease name:",
            placeholder="e.g., Diabetes, Fever, Headache, Pneumonia",
            key="disease_search"
        )
    
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    if search_button and disease_search:
        matches = fuzzy_search(disease_search, [d['name'] for d in diseases_db], threshold=60)
        
        if matches:
            st.session_state.search_history.append(f"Disease: {disease_search}")
            
            for match in matches[:5]:
                disease = next((d for d in diseases_db if d['name'].lower() == match.lower()), None)
                
                if disease:
                    with st.expander(f"📋 {disease['name']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**Disease Information:**")
                            st.markdown(f"**Category:** {disease.get('category', 'Unknown')}")
                            st.markdown(f"**Severity:** {disease.get('severity', 'Unknown')}")
                            st.markdown(f"**Transmission:** {disease.get('transmission', 'N/A')}")
                        
                        with col2:
                            st.markdown("**Symptoms:**")
                            for symptom in disease.get('symptoms', [])[:5]:
                                st.markdown(f"• {symptom}")
                        
                        with col3:
                            st.markdown("**Causes:**")
                            for cause in disease.get('causes', [])[:5]:
                                st.markdown(f"• {cause}")
                        
                        st.markdown("---")
                        st.markdown("**Recommended Medicines:**")
                        
                        recommended_meds = disease.get('recommended_medicines', [])
                        if recommended_meds:
                            for med_name in recommended_meds[:5]:
                                medicine = next((m for m in medicines_db if m['name'].lower() == med_name.lower()), None)
                                if medicine:
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    with col1:
                                        st.markdown(f"**💊 {medicine['name']}**")
                                    with col2:
                                        st.markdown(f"*{medicine.get('dosage', 'N/A')}*")
                                    with col3:
                                        st.caption(medicine.get('availability', 'Prescription'))
                        else:
                            st.info("No specific medicines recommended. Consult a doctor.")
                        
                        # Safety checks
                        if existing_conditions:
                            warnings = checker.check_contraindications(
                                recommended_meds,
                                existing_conditions
                            )
                            if warnings:
                                st.markdown("---")
                                for warning in warnings:
                                    st.warning(warning)
        else:
            st.error("❌ Disease not found. Please try another search or browse the knowledge base.")
            st.info("💡 Tip: Use the Disease Knowledge Base tab to explore all available diseases.")
    
    if not disease_search:
        st.info("👇 Enter a disease name above to get started.")

# TAB 2: Search by Medicine
with tab2:
    st.header("💊 Search by Medicine")
    st.write("Enter a medicine name to find its uses, side effects, interactions, and more.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        medicine_search = st.text_input(
            "Enter medicine name:",
            placeholder="e.g., Paracetamol, Ibuprofen, Aspirin, Amoxicillin",
            key="medicine_search"
        )
    
    with col2:
        search_button2 = st.button("🔍 Search", use_container_width=True, key="med_search_btn")
    
    if search_button2 and medicine_search:
        matches = fuzzy_search(medicine_search, [m['name'] for m in medicines_db], threshold=60)
        
        if matches:
            st.session_state.search_history.append(f"Medicine: {medicine_search}")
            
            for match in matches[:5]:
                medicine = next((m for m in medicines_db if m['name'].lower() == match.lower()), None)
                
                if medicine:
                    with st.expander(f"💊 {medicine['name']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**Medicine Details:**")
                            st.markdown(f"**Dosage:** {medicine.get('dosage', 'N/A')}")
                            st.markdown(f"**Category:** {medicine.get('category', 'N/A')}")
                            st.markdown(f"**Availability:** {medicine.get('availability', 'Prescription')}")
                        
                        with col2:
                            st.markdown("**Price & Storage:**")
                            st.markdown(f"**Price:** {medicine.get('price', 'N/A')}")
                            st.markdown(f"**Storage:** {medicine.get('storage', 'Room temperature')}")
                        
                        with col3:
                            st.markdown("**Precautions:**")
                            st.markdown(medicine.get('precautions', 'Consult doctor'))
                        
                        st.markdown("---")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Uses/Indications:**")
                            for use in medicine.get('uses', []):
                                st.markdown(f"✓ {use}")
                        
                        with col2:
                            st.markdown("**Side Effects:**")
                            for effect in medicine.get('side_effects', []):
                                st.markdown(f"⚠️ {effect}")
                        
                        st.markdown("---")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Contraindications:**")
                            for contra in medicine.get('contraindications', []):
                                st.markdown(f"🚫 {contra}")
                        
                        with col2:
                            st.markdown("**Drug Interactions:**")
                            for inter in medicine.get('interactions', []):
                                st.markdown(f"⚡ {inter}")
                        
                        # Interaction check if user has current meds
                        if current_medications:
                            st.markdown("---")
                            interactions = checker.check_interactions(
                                [medicine['name']],
                                current_medications
                            )
                            if interactions:
                                for interaction in interactions:
                                    st.error(interaction)
                            else:
                                st.success("✓ No interactions with your current medications")
        else:
            st.error("❌ Medicine not found.")
    
    if not medicine_search:
        st.info("👇 Enter a medicine name above to get started.")

# TAB 3: Disease Knowledge Base
with tab3:
    st.header("📚 Disease Knowledge Base")
    st.write("Explore and learn about diseases from around the world. This is for educational purposes.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category:",
            ["All"] + sorted(list(set(d.get('category', 'Other') for d in diseases_db))),
            key="disease_category"
        )
    
    with col2:
        severity_filter = st.selectbox(
            "Filter by Severity:",
            ["All", "Mild", "Mild-Moderate", "Moderate", "Moderate-Severe", "Severe", "Critical", "Chronic"],
            key="disease_severity"
        )
    
    with col3:
        search_disease = st.text_input("Search disease:", placeholder="Search...", key="disease_kb_search")
    
    # Filter diseases
    filtered_diseases = diseases_db.copy()
    
    if category_filter != "All":
        filtered_diseases = [d for d in filtered_diseases if d.get('category', 'Other') == category_filter]
    
    if severity_filter != "All":
        filtered_diseases = [d for d in filtered_diseases if severity_filter.lower() in d.get('severity', 'Unknown').lower()]
    
    if search_disease:
        filtered_diseases = [d for d in filtered_diseases if search_disease.lower() in d['name'].lower()]
    
    st.markdown(f"**Found: {len(filtered_diseases)} diseases**")
    
    # Display diseases in a nice format
    if filtered_diseases:
        cols = st.columns(3)
        
        for idx, disease in enumerate(filtered_diseases):
            col = cols[idx % 3]
            
            with col:
                with st.container():
                    st.markdown(f"### {disease['name']}")
                    st.markdown(f"🏷️ **Category:** {disease.get('category', 'Unknown')}")
                    st.markdown(f"⚠️ **Severity:** {disease.get('severity', 'Unknown')}")
                    st.markdown(f"🔹 **Top Symptoms:** {', '.join(disease.get('symptoms', [])[:2])}...")
                    
                    if st.button(f"📖 Learn More", key=f"disease_{disease['name']}"):
                        with st.expander(f"📋 {disease['name']} - Full Details"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Symptoms:**")
                                for symptom in disease.get('symptoms', []):
                                    st.markdown(f"• {symptom}")
                                
                                st.markdown("**Causes:**")
                                for cause in disease.get('causes', []):
                                    st.markdown(f"• {cause}")
                            
                            with col2:
                                st.markdown("**Prevention:**")
                                for prev in disease.get('prevention', []):
                                    st.markdown(f"• {prev}")
                                
                                st.markdown("**Transmission:**")
                                st.markdown(disease.get('transmission', 'N/A'))
                            
                            st.markdown("---")
                            st.markdown("**Treatment & Recommended Medicines:**")
                            for med in disease.get('recommended_medicines', [])[:5]:
                                st.markdown(f"💊 {med}")
    else:
        st.info("No diseases found with selected filters.")

# TAB 4: Symptom Checker
with tab4:
    st.header("🩺 Symptom Checker")
    st.write("Describe your symptoms in natural language and AI will suggest possible conditions and medicines.")
    
    symptom_input = st.text_area(
        "Describe your symptoms:",
        placeholder="e.g., 'I have a severe headache, fever, and body aches for 2 days'",
        height=100,
        key="symptom_input"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analyze_button = st.button("🔍 Analyze Symptoms", use_container_width=True)
    
    with col2:
        st.empty()
    
    with col3:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    if analyze_button and symptom_input:
        st.session_state.search_history.append(f"Symptom: {symptom_input}")
        
        # Extract symptoms using NLP
        extracted_symptoms = extractor.extract_symptoms(symptom_input)
        
        if extracted_symptoms:
            st.success(f"✓ Detected symptoms: {', '.join(extracted_symptoms)}")
            
            # Find matching diseases
            matching_diseases = matcher.find_diseases_by_symptoms(extracted_symptoms)
            
            if matching_diseases:
                st.markdown("---")
                st.subheader("🏥 Potential Conditions:")
                
                for disease in matching_diseases[:5]:
                    with st.expander(f"🏥 {disease['name']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"**Match Score:** {disease.get('match_score', 'N/A')}%")
                            st.markdown(f"**Category:** {disease.get('category', 'Unknown')}")
                        
                        with col2:
                            st.markdown(f"**Severity:** {disease.get('severity', 'Unknown')}")
                            st.markdown(f"**Transmission:** {disease.get('transmission', 'N/A')}")
                        
                        with col3:
                            st.markdown("**Your Symptoms Match:**")
                            for symptom in disease.get('matching_symptoms', []):
                                st.markdown(f"✓ {symptom}")
                        
                        st.markdown("---")
                        st.markdown("**Recommended Medicines:**")
                        
                        for med_name in disease.get('recommended_medicines', [])[:3]:
                            medicine = next((m for m in medicines_db if m['name'].lower() == med_name.lower()), None)
                            if medicine:
                                st.markdown(f"💊 **{medicine['name']}** - {medicine.get('dosage', 'N/A')}")
                                st.caption(medicine.get('precautions', 'Consult doctor'))
                        
                        # Safety warnings
                        if existing_conditions:
                            warnings = checker.check_contraindications(
                                disease.get('recommended_medicines', []),
                                existing_conditions
                            )
                            if warnings:
                                for warning in warnings:
                                    st.warning(warning)
                
                st.markdown("---")
                st.warning("⚠️ This is for informational purposes only. Please consult a healthcare professional for proper diagnosis.")
            else:
                st.info("No specific diseases matched. Please consult a doctor.")
        else:
            st.warning("Could not extract symptoms. Please describe more clearly.")
    
    if not symptom_input:
        st.info("👇 Describe your symptoms above to get started.")

# TAB 5: Interaction Checker
with tab5:
    st.header("⚠️ Medicine Interaction Checker")
    st.write("Check for dangerous interactions between medicines before taking them together.")
    
    selected_medicines = st.multiselect(
        "Select medicines to check:",
        sorted([m['name'] for m in medicines_db]),
        key="interaction_checker"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        check_button = st.button("🔍 Check Interactions", use_container_width=True)
    
    if check_button:
        if len(selected_medicines) >= 2:
            st.markdown("---")
            
            # Get interactions
            interactions = checker.check_interactions(selected_medicines, [])
            
            if interactions:
                st.error("⚠️ **WARNING: Interactions Found**")
                for interaction in interactions:
                    st.error(f"🚫 {interaction}")
            else:
                st.success("✓ No major interactions found between selected medicines.")
            
            # Show detailed info for each medicine
            st.markdown("---")
            st.subheader("📋 Medicine Details:")
            
            for med_name in selected_medicines:
                medicine = next((m for m in medicines_db if m['name'].lower() == med_name.lower()), None)
                if medicine:
                    with st.expander(f"💊 {medicine['name']}"):
                        st.markdown(f"**Dosage:** {medicine.get('dosage', 'N/A')}")
                        st.markdown(f"**Category:** {medicine.get('category', 'N/A')}")
                        st.markdown(f"**Availability:** {medicine.get('availability', 'N/A')}")
                        
                        st.markdown("**Side Effects:**")
                        for effect in medicine.get('side_effects', []):
                            st.markdown(f"• {effect}")
                        st.markdown("**Contraindications:**")
                        for contra in medicine.get('contraindications', []):
                            st.markdown(f"• {contra}")
        elif len(selected_medicines) == 1:
            st.warning("Please select at least 2 medicines to check interactions.")
        else:
            st.warning("Please select medicines to check interactions.")
    
    if not selected_medicines:
        st.info("👇 Select medicines above to check for interactions.")

# TAB 6: Medicine Directory
with tab6:
    st.header("📖 Medicine Directory")
    st.write("Browse all available medicines with detailed information.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_med = st.selectbox(
            "Filter by Category:",
            ["All"] + sorted(list(set(m.get('category', 'Other') for m in medicines_db))),
            key="med_category"
        )
    
    with col2:
        availability_med = st.selectbox(
            "Filter by Availability:",
            ["All", "OTC", "Prescription", "Both"],
            key="med_availability"
        )
    
    with col3:
        search_med = st.text_input(
            "Search medicine:",
            placeholder="Search...",
            key="med_directory_search"
        )
    
    # Filter medicines
    filtered_meds = medicines_db.copy()
    
    if category_med != "All":
        filtered_meds = [m for m in filtered_meds if m.get('category', 'Other') == category_med]
    
    if availability_med != "All":
        filtered_meds = [m for m in filtered_meds if availability_med.lower() in m.get('availability', 'prescription').lower()]
    
    if search_med:
        filtered_meds = [m for m in filtered_meds if search_med.lower() in m['name'].lower()]
    
    st.markdown(f"**Found: {len(filtered_meds)} medicines**")
    
    # Display medicines
    if filtered_meds:
        for idx, medicine in enumerate(filtered_meds[:50]):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{medicine['name']}**")
                st.caption(f"Category: {medicine.get('category', 'N/A')}")
            
            with col2:
                st.markdown(f"Dosage: {medicine.get('dosage', 'N/A')}")
            
            with col3:
                st.markdown(f"Avail: {medicine.get('availability', 'N/A')}")
            
            with col4:
                if st.button(f"📖 View", key=f"view_med_{idx}"):
                    with st.expander(f"📖 {medicine['name']} - Full Information"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Basic Information:**")
                            st.markdown(f"**Dosage:** {medicine.get('dosage', 'N/A')}")
                            st.markdown(f"**Category:** {medicine.get('category', 'N/A')}")
                            st.markdown(f"**Availability:** {medicine.get('availability', 'N/A')}")
                            st.markdown(f"**Price:** {medicine.get('price', 'N/A')}")
                            st.markdown(f"**Storage:** {medicine.get('storage', 'N/A')}")
                        
                        with col2:
                            st.markdown("**Usage Information:**")
                            st.markdown("**Uses:**")
                            for use in medicine.get('uses', []):
                                st.markdown(f"✓ {use}")
                        
                        st.markdown("---")
                        st.markdown("**Side Effects:**")
                        for effect in medicine.get('side_effects', []):
                            st.markdown(f"• {effect}")
                        
                        st.markdown("**Precautions:** " + medicine.get('precautions', 'N/A'))
    else:
        st.info("No medicines found with selected filters.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9em;">
    <p>💊 <strong>Pharmaceutical AI Advisor</strong> | Built with ❤️ for better healthcare accessibility</p>
    <p>⚠️ <strong>DISCLAIMER:</strong> This application is for educational purposes only and is NOT a substitute for professional medical advice.</p>
    <p>© 2024 | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
