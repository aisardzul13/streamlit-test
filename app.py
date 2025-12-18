import streamlit as st
import random
import requests
from datetime import datetime
from fpdf import FPDF
import base64

# Page configuration
st.set_page_config(
    page_title="Visionary 2030 | 5-Year Life Planner",
    page_icon="🚀",
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
        color: #1E1E1E; 
        border-left: 5px solid #FF4B4B; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- PDF GENERATOR FUNCTION ---
def generate_pdf(name, age, career, location, dream, roadmap):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(200, 10, txt="VISIONARY 2030: STRATEGIC BLUEPRINT", ln=True, align='C')
    pdf.ln(10)
    
    # Profile Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="PERSONAL PROFILE", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age} | Industry: {career}", ln=True)
    pdf.cell(200, 10, txt=f"Location: {location}", ln=True)
    pdf.ln(5)
    
    # The Dream
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="THE GRAND VISION", ln=True)
    pdf.set_font("Arial", 'I', 12)
    pdf.multi_cell(0, 10, txt=f'"{dream}"')
    pdf.ln(5)
    
    # The Roadmap
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="5-YEAR STRATEGIC ROADMAP", ln=True)
    
    for year, details in roadmap.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=year, ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 7, txt=details)
        pdf.ln(3)
    
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt=f"Generated on {datetime.now().strftime('%d %B %Y')}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- WEATHER ENGINE ---
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
        code = data['current_weather']['weathercode']
        condition = "Clear Skies" if code == 0 else "Cloudy" if code < 51 else "Rainy"
        return f"{temp}°C", condition
    except:
        return "N/A", "Unknown"

# --- SIDEBAR ---
st.sidebar.header("👤 Your Profile")
name = st.sidebar.text_input("Full Name", placeholder="e.g. Aisar")
age = st.sidebar.number_input("Current Age", min_value=0, max_value=120, value=25)
career = st.sidebar.text_input("Current Industry", placeholder="e.g. Software Engineering")

malaysian_states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu", "W.P. Kuala Lumpur", "W.P. Labuan", "W.P. Putrajaya"]
location = st.sidebar.selectbox("Home State", options=sorted(malaysian_states))

dream = st.sidebar.text_area("The 5-Year Grand Vision")

# --- HEADER ---
now = datetime.now()
current_time = now.strftime("%I:%M %p")
current_date = now.strftime("%A, %d %B %Y")
temp, condition = get_weather(location)

hour = now.hour
greeting = "Good Morning ☀️" if hour < 12 else "Good Afternoon 🌤️" if hour < 17 else "Good Evening 🌙"

t1, t2 = st.columns([2, 1])
with t1:
    st.title(f"{greeting}, {name if name else 'Visionary'}!")
    st.markdown("### 🚀 Your journey to 2030 begins today.")
with t2:
    st.markdown(f"""
    <div class="weather-box">
        📅 <b>{current_date}</b><br>
        ⏰ <b>Time: {current_time}</b><br>
        🌡️ <b>{location}: {temp} ({condition})</b>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- CONTENT ENGINE ---
if name and career and dream:
    # Defining the Roadmap Content for Display & PDF
    roadmap_content = {
        "YEARS 1 & 2: THE FOUNDATION": (
            "- Intensive Skill Mastery: Dedicate 10+ hours weekly to mastering core industry skills.\n"
            "- Financial Runway: Build a 6-month 'Vision Fund' to enable future risk-taking.\n"
            "- Strategic Networking: Connect with 2 mentors monthly who are already where you want to be.\n"
            "- Brand Building: Document your learning journey publicly (LinkedIn/Portfolio)."
        ),
        "YEARS 3 & 4: THE ACCELERATION": (
            "- Authority Shift: Transition from 'doer' to 'leader' by taking on management or consultancy roles.\n"
            "- Revenue Scaling: Launch a side income stream that leverages your primary expertise.\n"
            "- Life Systemization: Automate administrative tasks to free up energy for high-level strategy.\n"
            "- Physical Optimization: Peak your health to sustain the intensity of your 5th year leap."
        ),
        "YEAR 5: THE REALIZATION": (
            "- The Grand Transition: Execute the full move into your vision (new business, C-suite, etc.).\n"
            "- Harvest Season: Capitalize on the network and brand you have built over the last 48 months.\n"
            "- Wealth Management: Move from active earning to passive investment strategies.\n"
            "- Vision 2035: Set the trajectory for the next decade of your legacy."
        )
    }

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.subheader("🎯 Life Stage Analysis")
        if age < 25: focus = "Exploration & Skill-Stacking. Build a massive foundation while stakes are low."
        elif age < 40: focus = "Acceleration & Leverage. Shift from selling time to owning systems."
        else: focus = "Legacy & Freedom. Focus on mentorship, impact, and high-level strategy."
        st.info(focus)

    with col2:
        st.subheader("💭 The Manifested Goal")
        st.success(f"**“{dream}”**")

    st.divider()

    # Roadmap Visual
    st.header("🗺️ The Strategic 60-Month Roadmap")
    
    for year, text in roadmap_content.items():
        with st.expander(f"📅 {year}", expanded=(year.startswith("YEARS 1"))):
            st.markdown(text)

    # Export & Motivation Buttons
    st.divider()
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        if st.button("🔥 UNLEASH MOTIVATION 🔥"):
            st.balloons()
            motivations = [
                f"Listen {name}, it's {current_time}. While others are sleeping, you are building. The version of you in 5 years is already thanking you for not stopping today. Get after it!",
                f"{name}, you didn't come this far just to come this far. '{dream}' isn't just a sentence—it's your future reality. Take the first step in {location} today!",
                f"There are no rainy days for a man with a vision. Your discipline today in the {career} industry determines your freedom tomorrow. Own the day."
            ]
            st.info(random.choice(motivations))

    with m_col2:
        pdf_bytes = generate_pdf(name, age, career, location, dream, roadmap_content)
        st.download_button(
            label="📄 DOWNLOAD MY 5-YEAR BLUEPRINT (PDF)",
            data=pdf_bytes,
            file_name=f"{name}_Vision_2030.pdf",
            mime="application/pdf"
        )

else:
    st.warning("👈 Enter your details in the sidebar to build your blueprint!")

st.markdown("---")
st.markdown("<p style='text-align: center;'>Built for the Bold | Visionary 2030</p>", unsafe_allow_html=True)