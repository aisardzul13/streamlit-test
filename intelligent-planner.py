import streamlit as st
from supabase import create_client, Client
import requests
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

# --- 1. ACCESS SECRETS ---
try:
    # url = st.secrets["SUPABASE_URL"]
    # key = st.secrets["SUPABASE_KEY"]
    gemini_api_key = st.secrets["GEMINI_KEY"]
except KeyError as e:
    st.error(f"Missing secret in secrets.toml: {e}")
    st.stop()

# --- 2. INITIALIZE CONNECTIONS ---
# supabase: Client = create_client(url, key)

genai.configure(api_key=gemini_api_key)
# FIX: Corrected model name to 1.5
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. PAGE CONFIG ---
st.set_page_config(
    page_title="Visionary AI | Minimal", 
    page_icon="»",
    layout="wide"
)

# Initialize Session States
if "ai_plan" not in st.session_state: st.session_state.ai_plan = ""
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "tasks" not in st.session_state: st.session_state.tasks = []

# --- 4. CSS: CYBER-MINIMALIST ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap');
    html, body, [class*="st-"] { font-family: 'Outfit', sans-serif; color: #cfd2d6; }
    h1 { font-family: 'Outfit', sans-serif !important; font-weight: 800 !important; font-size: 1.8rem !important; margin-bottom: 0px !important; }
    .stApp { background: #0a0b10; }
    .custom-card { background: rgba(255, 255, 255, 0.01); padding: 25px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.9rem; }
    .stButton>button { border-radius: 6px; background: transparent; color: #e2c275 !important; border: 1px solid #e2c275; text-transform: uppercase; }
    .stButton>button:hover { background: #e2c275; color: #000000 !important; }
    [data-testid="stMetricValue"] { font-family: 'IBM Plex Mono', monospace !important; color: #e2c275 !important; font-size: 1.2rem !important; }
    section[data-testid="stSidebar"] { background-color: #08090d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ENGINES ---

def create_pdf(name, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, f"VISIONARY ROADMAP: {name.upper()}", ln=True, align='C')
    pdf.line(20, 25, 190, 25)
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    clean_text = content.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, txt=clean_text, align='L')
    return pdf.output(dest='S').encode('latin-1')

def get_weather(state):
    coords = {"Selangor": (3.07, 101.51), "W.P. Kuala Lumpur": (3.13, 101.68), "Johor": (1.48, 103.74)}
    lat, lon = coords.get(state, (3.13, 101.68))
    try:
        data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True").json()
        return f"{data['current_weather']['temperature']}°C"
    except: return "N/A"

# def save_to_cloud(name, career, roadmap, pdf_bytes):
#     """Handles all Supabase uploads."""
#     try:
#         # 1. Database Insert
#         data = {"name": name, "career": career, "roadmap_text": roadmap}
#         supabase.table("profiles").insert(data).execute()

#         # 2. Storage Upload
#         file_path = f"{name}_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         supabase.storage.from_("roadmaps").upload(
#             path=file_path,
#             file=pdf_bytes,
#             file_options={"content-type": "application/pdf"}
#         )
#         st.success("Trajectory securely synced to cloud.")
#     except Exception as e:
#         st.error(f"Cloud Sync Error: {e}")

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown(" » SYSTEM CONFIG")
    name = st.text_input("Full Name", placeholder="Aisar")
    age = st.number_input("Age", min_value=1, value=25)
    career = st.text_input("Working Industry/Career", placeholder="AI Engineering")
    location = st.selectbox("Location", ["Selangor", "W.P. Kuala Lumpur", "Johor", "Pulau Pinang", "Sabah", "Sarawak"])
    vibe = st.selectbox("AI Persona", ["The Strategist", "The Realist", "The Mentor"])
    dream = st.text_area("2030 Vision")
    gen_btn = st.button("EXECUTE GENERATION")

# --- 7. HEADER & METRICS ---
temp = get_weather(location)
c_t, c_w = st.columns([3, 1])
with c_t:
    st.markdown(f"<h1>HELLO, <span style='color:#e2c275'>{name.upper() if name else 'VISIONARY'}</span>.</h1>", unsafe_allow_html=True)
with c_w:
    st.markdown(f"<div style='text-align: right;'>{datetime.now().strftime('%d.%m.%Y')} | <span style='color:#e2c275'>{temp}</span></div>", unsafe_allow_html=True)

st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("STATUS", "IDLE" if not st.session_state.ai_plan else "ACTIVE")
m2.metric("TARGET", "2030")
m3.metric("STYLE", vibe.split()[-1].upper())
m4.metric("TASKS", len([t for t in st.session_state.tasks if not t['done']]))
st.divider()

# --- 8. MAIN TABS ---
t1, t2, t3 = st.tabs(["STRATEGIC ROADMAP", "AI CONSULTANT", "MILESTONES"])

with t1:
    if gen_btn:
        if not name or not dream: 
            st.warning("Incomplete profile data.")
        else:
            with st.spinner("Architecting trajectory..."):
                prompt = f"Role: {vibe}. Generate a detailed, professional 5-year roadmap for {name}, a {age}-year-old in {career}, based in {location}. Vision: {dream}. Use clear year-by-year headers."
                response = model.generate_content(prompt)
                st.session_state.ai_plan = response.text
                
                # Create PDF & Save to Cloud
                pdf_data = create_pdf(name if name else "Visionary", st.session_state.ai_plan)
                save_to_cloud(name, career, st.session_state.ai_plan, pdf_data)

    if st.session_state.ai_plan:
        st.markdown(f'<div class="custom-card">{st.session_state.ai_plan}</div>', unsafe_allow_html=True)
        pdf_data = create_pdf(name if name else "Visionary", st.session_state.ai_plan)
        st.download_button("📄 DOWNLOAD FORMATTED PDF", data=pdf_data, file_name=f"{name}_Roadmap.pdf", mime="application/pdf")
    else:
        st.info("Input configuration and execute generation.")

with t2:
    if st.session_state.ai_plan:
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]): st.markdown(chat['content'])
        
        if user_in := st.chat_input("Query the system..."):
            st.session_state.chat_history.append({"role": "user", "content": user_in})
            res = model.generate_content(f"Plan: {st.session_state.ai_plan}. Question: {user_in}").text
            st.session_state.chat_history.append({"role": "assistant", "content": res})
            st.rerun()
    else: st.warning("Generate roadmap first.")

with t3:
    ci, cb = st.columns([0.8, 0.2])
    ti = ci.text_input("New Protocol:", placeholder="e.g. Master Cloud Architecture")
    if cb.button("COMMIT"):
        if ti:
            st.session_state.tasks.append({"task": ti, "done": False})
            st.rerun()
    
    for i, t in enumerate(st.session_state.tasks):
        cc, ct, cd = st.columns([0.05, 0.85, 0.1])
        st.session_state.tasks[i]["done"] = cc.checkbox("", value=t["done"], key=f"c_{i}")
        label = f"~~{t['task']}~~" if t['done'] else t['task']
        ct.markdown(label)
        if cd.button("DEL", key=f"d_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

st.markdown("<div style='text-align: center; color: #444; font-size: 0.6rem; margin-top: 50px;'>AISARDZUL | PROJECT_VISIONARY | 2025-2030</div>", unsafe_allow_html=True)