import streamlit as st
import random
import requests
from datetime import datetime

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
    .stButton>button:hover { background-color: #ff3333; color: white; }
    .weather-box {
        padding: 15px; border-radius: 15px; background: #ffffff;
        border-left: 5px solid #FF4B4B; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_weather(state):
    # Mapping Malaysian states to approximate lat/lon for Open-Meteo API
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
        # Simple weather code mapping
        condition = "Sunny" if code == 0 else "Cloudy" if code < 51 else "Raining"
        return f"{temp}°C", condition
    except:
        return "N/A", "Unknown"

# --- SIDEBAR ---
st.sidebar.header("👤 Personal Profile")
name = st.sidebar.text_input("Name", placeholder="e.g. Aisar")
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)
career = st.sidebar.text_input("Industry", placeholder="e.g. Tech")

malaysian_states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu", "W.P. Kuala Lumpur", "W.P. Labuan", "W.P. Putrajaya"]
location = st.sidebar.selectbox("Location", options=sorted(malaysian_states))

dream = st.sidebar.text_area("Your 5-Year Goal")

# --- TOP SECTION: DATE, TIME & WEATHER ---
now = datetime.now()
current_time = now.strftime("%H:%M")
current_date = now.strftime("%A, %d %B %Y")
temp, condition = get_weather(location)

# Dynamic Greeting
hour = now.hour
if hour < 12: greeting = "Selamat Pagi ☀️"
elif hour < 17: greeting = "Selamat Tengahari 🌤️"
else: greeting = "Selamat Malam 🌙"

# Header Layout
t1, t2 = st.columns([2, 1])
with t1:
    st.title(f"{greeting}, {name if name else 'Visionary'}!")
    st.subheader("🚀 Visionary 2030: Your 5-Year Blueprint")
with t2:
    st.markdown(f"""
    <div class="weather-box">
        <b>📅 {current_date}</b><br>
        <b>⏰ Local Time: {current_time}</b><br>
        <b>🌡️ {location}: {temp} ({condition})</b>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- MAIN LOGIC ---
if name and career and dream:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🎯 Strategic Focus")
        if age < 25:
            focus = "The Foundation Phase: Focus on 'Skill-Stacking' and networking in KL."
        elif age < 40:
            focus = "The Acceleration Phase: Build deep expertise and lead projects."
        else:
            focus = "The Legacy Phase: Optimize systems and mentor the next generation."
        st.info(focus)
        st.write(f"Today is a great day to work on this, given the {condition.lower()} weather in {location}!")

    with col2:
        st.subheader("💭 The North Star")
        st.success(f"**“{dream}”**")

    st.divider()

    # --- ROADMAP ---
    st.header("🗺️ Your Detailed 60-Month Roadmap")
    with st.expander("📅 Years 1–2: Mastery", expanded=True):
        st.write(f"Focus on becoming a top performer in **{career}**. Start building your 'Vision Fund' and find 3 mentors.")
    with st.expander("📅 Years 3–4: Scaling"):
        st.write(f"Transition to leadership. Your goal is to make **{dream}** 50% of your daily reality.")
    with st.expander("📅 Year 5: Realization"):
        st.write(f"The 'Big Leap'. Execute your master plan and look back at your progress since {now.year}.")

    # --- MOTIVATION ---
    st.divider()
    if st.button("🔥 Ignite My Motivation 🔥"):
        st.balloons()
        msgs = [
            f"Listen {name}, it's {current_time} on a {now.strftime('%A')}. Most people are scrolling; you are planning. That alone makes you dangerous. Don't stop.",
            f"The {condition.lower()} weather in {location} today is just a backdrop. Your internal fire for '{dream}' is what matters. Get to work.",
            f"Five years from now, you will arrive. The question is: Where? Stick to this plan and you'll arrive exactly where you want to be."
        ]
        st.markdown(f"### ⚡ Message:")
        st.write(random.choice(msgs))

else:
    st.warning("👈 Enter your details in the sidebar to begin!")

st.markdown("---")
st.markdown("<p style='text-align: center;'>Built for Malaysian Dreamers 🇲🇾</p>", unsafe_allow_html=True)