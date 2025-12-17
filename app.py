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

# Custom CSS for a professional, readable UI
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
    .plan-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

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
career = st.sidebar.text_input("Current Industry", placeholder="e.g. Data Science / Finance")

malaysian_states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu", "W.P. Kuala Lumpur", "W.P. Labuan", "W.P. Putrajaya"]
location = st.sidebar.selectbox("Home State", options=sorted(malaysian_states))

dream = st.sidebar.text_area("The 5-Year Grand Vision", placeholder="Describe exactly what your life looks like in 5 years...")

# --- HEADER SECTION ---
now = datetime.now()
current_time = now.strftime("%I:%M %p")
current_date = now.strftime("%A, %d %B %Y")
temp, condition = get_weather(location)

hour = now.hour
greeting = "Good Morning ☀️" if hour < 12 else "Good Afternoon 🌤️" if hour < 17 else "Good Evening 🌙"

t1, t2 = st.columns([2, 1])
with t1:
    st.title(f"{greeting}, {name if name else 'Visionary'}!")
    st.markdown(f"### 🚀 Welcome to your future. \nToday is the first day of your next 5 years.")
with t2:
    st.markdown(f"""
    <div class="weather-box">
        📅 <b>{current_date}</b><br>
        ⏰ <b>Time: {current_time}</b><br>
        🌡️ <b>{location}: {temp} ({condition})</b>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- MAIN ENGINE ---
if name and career and dream:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🎯 Life Stage Analysis")
        if age < 25:
            stage = "The Exploration & Skill-Stacking Phase"
            desc = "You are in the high-energy season. Your goal is to acquire as many 'Meta-Skills' (coding, sales, writing) as possible. Don't fear failure; fear stagnation."
        elif age < 40:
            stage = "The Acceleration & Leverage Phase"
            desc = "This is your prime earning window. Focus on moving from 'selling time' to 'owning systems.' Use your expertise in your industry to lead and scale."
        else:
            stage = "The Legacy & Freedom Phase"
            desc = "Prioritize high-impact work and mentoring. Your 5-year goal should center on building freedom—both financial and time-based."
        
        st.info(f"**{stage}**\n\n{desc}")

    with col2:
        st.subheader("💭 The Manifested Goal")
        st.success(f"**“{dream}”**")
        st.write(f"This vision is achievable. The climate in {location} today is {condition.lower()}, but your internal climate is purely determined by your discipline.")

    st.divider()

    # --- THE DETAILED ROADMAP ---
    st.header("🗺️ The Strategic 60-Month Roadmap")

    # Year 1-2
    with st.expander("📅 Years 1 & 2: Building the Unshakable Foundation", expanded=True):
        st.markdown(f"""
        * **Intensive Skill Mastery:** Spend 10 hours a week outside of work mastering the top 3 skills needed in **{career}**.
        * **The Vision Fund:** Set up a dedicated savings account. Aim to have 6 months of living expenses by the end of Year 2 to provide "Risk Capital."
        * **Network Expansion:** Connect with at least 2 people a month who are already living your dream. In {location}, seek out local meetups or digital communities.
        * **Identity Shift:** Stop saying "I want to be..." and start saying "I am a..." Document your progress on LinkedIn to build a professional brand.
        """)

    # Year 3-4
    with st.expander("📅 Years 3 & 4: Scaling and Market Domination"):
        st.markdown(f"""
        * **Leverage & Authority:** Shift from being the person who 'does' to the person who 'leads.' Seek out management roles or launch your own consultancy.
        * **Revenue Diversification:** Create a side income stream related to **{career}**. Your goal is to have your 'side' income cover 30% of your expenses by Year 4.
        * **Systemization:** Start automating your life. Use tools, delegating, or software to free up your mental energy for the 'Big Leap' in Year 5.
        * **Health & Energy:** Optimize your physical performance. You cannot run a marathon in the final year if your engine is broken.
        """)

    # Year 5
    with st.expander("📅 Year 5: The Grand Execution & Realization"):
        st.markdown(f"""
        * **The Transition:** This is the year you move full-time into your dream of **"{dream}"**. Whether it's a new company, a business launch, or a lifestyle shift—it happens now.
        * **Harvesting Results:** The networking and branding you did in Year 1-2 now pays off. Opportunities should start seeking you out, rather than you chasing them.
        * **Wealth Optimization:** Move from 'Saving' to 'Investing.' Ensure your assets are working as hard as you did for the last 4 years.
        * **The Next Peak:** Spend the final 3 months of Year 5 designing your 10-year vision. You have arrived; now look further.
        """)

    # --- UPLIFTING MOTIVATION ---
    st.divider()
    if st.button("🔥 UNLEASH MOTIVATION 🔥"):
        st.balloons()
        
        motivations = [
            f"**Listen, {name}.** Right now, it's {current_time}. Most people are waiting for 'one day' to start. They are waiting for the perfect weather in {location} or the perfect economy. But you? You just built a map. You have the industry knowledge of **{career}** and a hunger for **{dream}**. The version of you that exists in 5 years is looking back at you right now, thanking you for not giving up today. You aren't just a dreamer; you're an architect. **Now, build it.**",
            
            f"**{name}, the world is loud, but your vision must be louder.** In 60 months, you will be {age + 5} years old. Time is the only resource we can't buy back. Do not waste another second doubting if you are capable of achieving **{dream}**. You were given that dream because you have the capacity to fulfill it. Take that first step in {location} today. Small, boring, daily wins are the bricks that build empires. **Go get yours.**",
            
            f"**This is your wake-up call, {name}.** The path to **{dream}** isn't a straight line—it's a battlefield. There will be rainy days in {location} and moments of doubt in your **{career}** journey. But remember: a diamond is just a piece of charcoal that handled stress exceptionally well. You are in your {stage.lower()}. This is your time to shine. Don't settle for a life that is less than the one you are capable of living. **The future belongs to the bold.**"
        ]
        
        st.markdown(f"### ⚡ A Personal Message for You:")
        st.info(random.choice(motivations))
        st.caption("“The best way to predict the future is to create it.”")

else:
    st.warning("👈 The roadmap to 2030 is ready. Fill in your details on the left to unlock it!")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Built with 🚀 for Visionaries | Keep Pushing.</p>", unsafe_allow_html=True)