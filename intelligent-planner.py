import streamlit as st
import random
import requests
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

# --- API CONFIGURATION ---
# Replace with your actual API key if needed
GEMINI_API_KEY = "AIzaSyDPbHNSw_1Qz6_XsMKaoyT8oTNAohznFmE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Page configuration
st.set_page_config(page_title="Visionary AI 3.1", page_icon="🔥", layout="wide")

# Initialize Session States
if "ai_plan" not in st.session_state: st.session_state.ai_plan = ""
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "tasks" not in st.session_state: st.session_state.tasks = []

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3em;
        background-color: #FF4B4B; color: white; font-weight: bold; border: none;
    }
    .weather-box {
        padding: 15px; border-radius: 15px; background-color: #ffffff;
        color: #1E1E1E; /* Dark text for visibility */
        border-left: 5px solid #FF4B4B; 
        box-shadow: 0px 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- WEATHER ENGINE ---
def get_weather(state):
    coords = {"Selangor": (3.07, 101.51), "W.P. Kuala Lumpur": (3.13, 101.68), "Johor": (1.48, 103.74), "Pulau Pinang": (5.41, 100.32), "Sabah": (5.97, 116.07), "Sarawak": (1.55, 110.33)}
    lat, lon = coords.get(state, (3.13, 101.68))
    try:
        data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True").json()
        return f"{data['current_weather']['temperature']}°C"
    except: return "N/A"

# --- SIDEBAR: BLANK INPUTS ---
st.sidebar.title("🛠️ Control Center")
name = st.sidebar.text_input("Full Name", value="", placeholder="Enter your name...")
age = st.sidebar.number_input("Current Age", min_value=0, max_value=120, value=0)
career = st.sidebar.text_input("Current Industry/Job", value="", placeholder="e.g. Graphic Designer")
location = st.sidebar.selectbox("Home State", ["Selangor", "W.P. Kuala Lumpur", "Johor", "Pulau Pinang", "Sabah", "Sarawak", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Terengganu"])
vibe = st.sidebar.selectbox("AI Personality Mode", ["Supportive Coach", "Strict Disciplinarian", "Financial Strategist"])
dream = st.sidebar.text_area("Your 5-Year Master Goal", value="", placeholder="What is your ultimate vision for 2030?")

# --- TOP BAR ---
temp = get_weather(location)
st.title("🚀 Visionary AI 3.1")
st.markdown(f"**{datetime.now().strftime('%d %B %Y')} | Local Weather in {location}: {temp}**")
st.divider()

# --- MAIN LAYOUT ---
tab1, tab2, tab3 = st.tabs(["📋 My Blueprint", "💬 AI Chatbot", "✅ Goal Tracker"])

# --- TAB 1: THE BLUEPRINT ---
with tab1:
    if st.sidebar.button("✨ GENERATE MY FUTURE ✨"):
        if not name or not career or not dream or age == 0:
            st.warning("⚠️ Please fill in all profile details in the sidebar first!")
        else:
            vibe_prompts = {
                "Supportive Coach": "Be empathetic, warm, and focus on steady growth and mental well-being.",
                "Strict Disciplinarian": "Be blunt, no-nonsense, and focus on hard work and discipline. Call out laziness.",
                "Financial Strategist": "Focus on ROI, capital accumulation, and market trends in Malaysia."
            }
            
            prompt = f"You are a {vibe}. {vibe_prompts[vibe]} Create a professional 5-year roadmap for {name}, age {age}, working in {career}, based in {location}, Malaysia. Goal: {dream}. Use headers and bullets."
            
            with st.spinner("Gemini is architecting your life..."):
                try:
                    response = model.generate_content(prompt)
                    st.session_state.ai_plan = response.text
                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")

    if st.session_state.ai_plan:
        st.markdown(st.session_state.ai_plan)
        
        # PDF Generation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"Visionary 2030: {name}'s Plan", ln=True, align='C')
        pdf.set_font("Arial", size=11)
        clean_text = st.session_state.ai_plan.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        
        st.download_button("📄 Download PDF Blueprint", data=pdf.output(dest='S').encode('latin-1'), file_name=f"{name}_Blueprint.pdf")
    else:
        st.info("The canvas is empty. Fill in your details in the sidebar and click 'Generate' to see your future.")

# --- TAB 2: AI CHAT ---
with tab2:
    st.subheader("💬 Deep Dive Consultation")
    if st.session_state.ai_plan:
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

        if user_input := st.chat_input("Ask a follow-up question..."):
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"): st.markdown(user_input)
            
            chat_context = f"Context: You just generated this 5-year plan for {name}: {st.session_state.ai_plan}. User asks: {user_input}"
            ai_response = model.generate_content(chat_context).text
            
            with st.chat_message("assistant"): st.markdown(ai_response)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    else:
        st.warning("Generate your blueprint first to unlock the AI Consultant.")

# --- TAB 3: GOAL TRACKER ---
with tab3:
    st.subheader("🎯 Goal Execution Board")
    
    t_col1, t_col2 = st.columns([0.8, 0.2])
    new_task = t_col1.text_input("New Milestone:", placeholder="e.g. Complete my first coding cert")
    if t_col2.button("➕ Add Task"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})
            st.rerun()

    st.write("---")
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.1, 0.8, 0.1])
        is_done = cols[0].checkbox("", value=task["done"], key=f"task_check_{i}")
        st.session_state.tasks[i]["done"] = is_done
        
        if is_done:
            cols[1].markdown(f"~~{task['task']}~~")
        else:
            cols[1].write(task["task"])
            
        if cols[2].button("🗑️", key=f"task_del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- CUSTOM FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>aisardzul | Built for the Visionaries | 2025-2030</p>", unsafe_allow_html=True)