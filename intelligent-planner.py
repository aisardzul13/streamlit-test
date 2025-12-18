import streamlit as st
import random
import requests
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

# --- API CONFIGURATION ---
# Ensure your library is updated to avoid the 404 error
GEMINI_API_KEY = "AIzaSyDPbHNSw_1Qz6_XsMKaoyT8oTNAohznFmE"
genai.configure(api_key=GEMINI_API_KEY)

# Use the stable model string
model = genai.GenerativeModel('gemini-2.5-flash')

# Page configuration
st.set_page_config(
    page_title="Visionary AI | 5-Year Life Planner",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 25px; height: 3.5em;
        background-color: #FF4B4B; color: white; font-weight: bold;
        border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff3333; color: white; box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4); }
    
    .weather-box {
        padding: 20px; 
        border-radius: 15px; 
        background-color: #ffffff;
        color: #1E1E1E; /* FIXED: Dark color so you can see the text! */
        border-left: 5px solid #FF4B4B; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True) # FIXED: changed allow_items to allow_html

# --- HELPER FUNCTIONS ---
def get_weather(state):
    coords = {
        "Selangor": (3.07, 101.51), "W.P. Kuala Lumpur": (3.13, 101.68),
        "Johor": (1.48, 103.74), "Pulau Pinang": (5.41, 100.32),
        "Sabah": (5.97, 116.07), "Sarawak": (1.55, 110.33),
        "Kedah": (6.12, 100.36), "Kelantan": (6.12, 102.23),
        "Melaka": (2.18, 102.24), "Negeri Sembilan": (2.72, 101.94),
        "Pahang": (3.81, 103.32), "Perak": (4.59, 101.09),
        "Perlis": (6.44, 100.20), "Terengganu": (5.33, 103.13),
        "W.P. Labuan": (5.28, 115.24), "W.P. Putrajaya": (2.92, 101.68)
    }
    lat, lon = coords.get(state, (3.13, 101.68))
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
        data = requests.get(url).json()
        temp = data['current_weather']['temperature']
        return f"{temp}°C", "Live"
    except:
        return "N/A", "Unknown"

def generate_pdf(name, plan_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Visionary 2030: {name}'s Blueprint", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    # Handle characters that might not exist in standard PDF fonts
    clean_text = plan_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR ---
st.sidebar.header("👤 Your Profile")
name = st.sidebar.text_input("Full Name")
age = st.sidebar.number_input("Current Age", min_value=1, value=25)
career = st.sidebar.text_input("Current Industry")
location = st.sidebar.selectbox("Home State", sorted(["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu", "W.P. Kuala Lumpur", "W.P. Labuan", "W.P. Putrajaya"]))
dream = st.sidebar.text_area("The 5-Year Grand Vision")

# --- HEADER ---
now = datetime.now()
temp, condition = get_weather(location)

t1, t2 = st.columns([2, 1])
with t1:
    st.title(f"🤖 AI Life Architect")
    st.subheader(f"Welcome, {name if name else 'Visionary'}!")
with t2:
    st.markdown(f"""
    <div class="weather-box">
        📅 <b>{now.strftime('%A, %d %B')}</b><br>
        ⏰ <b>{now.strftime('%I:%M %p')}</b><br>
        🌡️ <b>{location}: {temp}</b>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- GENERATION ---
if st.sidebar.button("✨ GENERATE AI BLUEPRINT ✨"):
    if name and career and dream:
        with st.spinner("Consulting the AI..."):
            try:
                prompt = f"Plan a 5-year roadmap for {name}, a {age} year old in {career}, living in {location}. Their goal is {dream}. Provide specific Malaysian context."
                response = model.generate_content(prompt)
                st.session_state.ai_plan = response.text
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.error("Please fill in all sidebar fields!")

if "ai_plan" in st.session_state:
    st.markdown(st.session_state.ai_plan)
    
    pdf_bytes = generate_pdf(name, st.session_state.ai_plan)
    st.download_button(
        label="📄 Download Blueprint (PDF)",
        data=pdf_bytes,
        file_name=f"{name}_Vision_2030.pdf",
        mime="application/pdf"
    )