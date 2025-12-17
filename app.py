import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Visionary 2030 | 5-Year Life Planner",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for a bit of flair
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_items=True)

st.title("🚀 Visionary 2030: Your 5-Year Blueprint")
st.write("Transform your dreams into a structured timeline. Let's design your future together!")

# --- SIDEBAR INPUTS ---
st.sidebar.header("👤 Personal Profile")
name = st.sidebar.text_input("What should we call you?", placeholder="e.g. Ali")
age = st.sidebar.number_input("How many laps around the sun?", min_value=0, max_value=120, value=25)
career = st.sidebar.text_input("Current field of work/study", placeholder="e.g. Digital Marketing")

# Malaysian States
malaysian_states = [
    "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", 
    "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", 
    "Terengganu", "W.P. Kuala Lumpur", "W.P. Labuan", "W.P. Putrajaya"
]
location = st.sidebar.selectbox("Where are you based?", options=sorted(malaysian_states))

st.sidebar.divider()
dream = st.sidebar.text_area(
    "Describe your ultimate 5-year goal:",
    placeholder="e.g. To lead a tech startup in KL while achieving total financial independence and traveling once a year..."
)

# --- MAIN LOGIC ---
if name and career and dream:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader(f"👋 Welcome, {name}!")
        st.info(f"📍 Currently navigating life in **{location}** within the **{career}** sector.")
        
        # Dynamic Focus Logic
        if age < 25:
            focus_title = "The Foundation Phase"
            focus_desc = "This is your time to fail fast and learn faster. Focus on 'skill-stacking'—combining different talents to become a unique asset in the Malaysian market."
        elif age < 40:
            focus_title = "The Acceleration Phase"
            focus_desc = "You are in your prime earning and networking years. Focus on building 'Social Capital' and deep expertise that makes you irreplaceable."
        else:
            focus_title = "The Legacy Phase"
            focus_desc = "Focus on optimizing your systems, mentoring the next generation, and ensuring your wealth works harder for you than you do for it."

        st.markdown(f"### 🎯 Your Primary Focus: \n**{focus_title}**")
        st.write(focus_desc)

    with col2:
        st.subheader("💭 The Vision")
        st.success(f"**“{dream}”**")
        st.write("This isn't just a dream; it's a destination. Below is the roadmap to get you there.")

    st.divider()

    # --- ENHANCED 5-YEAR PLAN ---
    st.header("🗺️ Your Strategic Roadmap")
    
    with st.expander("📅 Year 1 & 2: Skill Acquisition & Network Building", expanded=True):
        st.markdown(f"""
        * **Deep Dive:** Dedicate the first 18 months to becoming a 'Top 10%' performer in **{career}**. Attend industry meetups in {location} or KL to find a mentor.
        * **Identity Shift:** Start acting like the person who has already achieved "{dream}". Change your habits, your reading list, and your circle.
        * **Financial Runway:** Aim to save at least 3-6 months of emergency funds to give you the "bravery capital" needed for bigger moves later.
        """)

    with st.expander("📅 Year 3 & 4: Strategic Positioning & Scaling"):
        st.markdown(f"""
        * **Leverage:** Transition from 'doing the work' to 'designing the work.' Look for leadership roles or start your side-hustle/business officially.
        * **Visibility:** Start sharing your journey online (LinkedIn/Portfolio). Make sure the right people in Malaysia know your name and what you stand for.
        * **The Pivot:** By Year 4, 50% of your daily tasks should be directly related to your goal of **"{dream}"**.
        """)

    with st.expander("📅 Year 5: Realization & New Horizons"):
        st.markdown(f"""
        * **The Big Launch:** This is the year of execution. Whether it's a career jump, a business launch, or a lifestyle shift, this is where the groundwork pays off.
        * **Legacy & Systems:** Automate your income and your workflows. Ensure that your success is sustainable and not just a one-time peak.
        * **Full Integration:** Look back at your life in {location} 5 years ago and realize how much you've grown. It's time to set the vision for the next decade!
        """)

    # --- ENHANCED MOTIVATION ---
    st.divider()
    if st.button("✨ Ignite My Motivation ✨"):
        st.balloons()
        
        motivations = [
            f"Listen, {name}. The next five years will pass whether you take action or not. You can either be five years older with a collection of 'what ifs', or five years older with a life that reflects your courage. Your dream of '{dream}' isn't a burden; it's a compass. Trust it.",
            f"Hey {name}, remember that big things are built from small, boring daily wins. You don't need to see the whole staircase to take the first step in {location}. Discipline is simply choosing between what you want now and what you want most. Choose your future self.",
            f"The world in 2030 will look very different, {name}. You have the unique advantage of being in the {career} field right now. Don't just watch the change happen—be the one driving it. You are capable of more than you are currently giving yourself credit for."
        ]
        
        st.markdown(f"### 🚀 A Message for You:")
        st.write(random.choice(motivations))
        st.caption("“The best time to plant a tree was 20 years ago. The second best time is today.”")

else:
    st.warning("👈 Please enter your details and your dream in the sidebar to unlock your personalized roadmap!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ for dreamers in Malaysia. Stay consistent.")