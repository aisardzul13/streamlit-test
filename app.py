import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Visionary 2030 | 5-Year Life Planner",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3.5em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Visionary 2030: Your 5-Year Blueprint")
st.write("Stop dreaming in circles. Let's map out your trajectory for the next 60 months.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("👤 Personal Profile")
name = st.sidebar.text_input("What should we call you?", placeholder="e.g. Aisar")
age = st.sidebar.number_input("Current Age", min_value=0, max_value=120, value=25)
career = st.sidebar.text_input("Current Field / Industry", placeholder="e.g. Software Engineering")

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
    placeholder="e.g. To become a lead developer, own a home in Selangor, and have a side business generating RM5k monthly..."
)

# --- MAIN LOGIC ---
if name and career and dream:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader(f"✨ The Profile: {name}")
        st.info(f"📍 Based in **{location}** | 🛠️ Industry: **{career}**")
        
        # Dynamic Life Stage Logic
        if age < 25:
            focus_title = "The Foundation & Exploration Phase"
            focus_desc = "Now is the time for 'Aggressive Learning.' Since you are under 25, your goal is to build a massive skill-stack. Don't worry about being a specialist yet; be a polymath. Try new technologies, join networking events in KL, and fail as often as possible while the stakes are low."
        elif age < 40:
            focus_title = "The Acceleration & Mastery Phase"
            focus_desc = "You are in the 'Wealth Creation' window. Focus on deep-work and becoming a top-tier expert in your field. This phase is about leverage—using your network in Malaysia and your technical expertise to move from an individual contributor to a leader or business owner."
        else:
            focus_title = "The Legacy & System Phase"
            focus_desc = "Focus on 'Life Optimization.' Your 5-year goal should center on building systems that provide both financial freedom and time flexibility. At this stage, your experience is your greatest asset; consider mentoring, consulting, or investing in the next generation."

        st.markdown(f"### 🎯 Strategic Focus: \n**{focus_title}**")
        st.write(focus_desc)

    with col2:
        st.subheader("💭 The North Star")
        st.success(f"**“{dream}”**")
        st.write("This vision is your 'Why.' Every hard morning and late night over the next 5 years is an investment in making this specific sentence your reality.")

    st.divider()

    # --- EXPANDED 5-YEAR PLAN ---
    st.header("🗺️ Your Detailed 60-Month Roadmap")
    
    with st.expander("📅 Years 1–2: Mastery and Market Positioning", expanded=True):
        st.markdown(f"""
        * **Skill Audit:** Conduct a deep audit of the skills required for **"{dream}"**. Spend the first 12 months filling those gaps through certifications or project-based learning.
        * **Network Injection:** Don't just work in {location}; connect with it. Find 3 mentors who are 5 years ahead of where you want to be. 
        * **Personal Branding:** Start documenting your journey. Whether it's LinkedIn or a personal blog, make sure that by the end of Year 2, people in the **{career}** industry know who you are.
        * **Financial Foundation:** Automate your savings. If your goal requires capital, start a dedicated 'Vision Fund' today.
        """)

    with st.expander("📅 Years 3–4: Scaling and Authority"):
        st.markdown(f"""
        * **Transition to Leadership:** Move from execution to strategy. Seek out roles that require managing people, budgets, or complex systems.
        * **Income Diversification:** If your dream involves financial freedom, Year 3 is when you should launch a secondary income stream or a side-hustle that complements your career in **{career}**.
        * **Lifestyle Design:** Begin aligning your daily environment with your goal. If you want to live elsewhere or travel, start testing 'work-from-anywhere' setups or negotiating flexible terms.
        * **The 80/20 Rule:** Identify the 20% of your efforts producing 80% of your progress toward **"{dream}"** and double down on them.
        """)

    with st.expander("📅 Year 5: Realization and Transition"):
        st.markdown(f"""
        * **The Leap:** This is the year you execute the "Main Event"—whether that's quitting your job to start a business, buying that property in {location}, or stepping into a C-suite role.
        * **Audit and Reflection:** Look back at your profile from Year 1. You will likely find that you have surpassed your original expectations.
        * **Sustainability:** Ensure that the success you've built is sustainable. Focus on health, mental well-being, and family to ensure you can enjoy the fruits of your 5-year labor.
        * **Next Horizon:** By the end of this year, draft your 'Vision 2035' plan. Growth never stops!
        """)

    # --- EXTENDED MOTIVATION ---
    st.divider()
    if st.button("🔥 Generate High-Octane Motivation 🔥"):
        st.balloons()
        
        motivations = [
            f"Listen closely, {name}. The next 1,825 days are going to pass regardless of whether you are working toward your dream or just watching the clock. In five years, you will be {age + 5} years old. You can either be {age + 5} with the life you described—'{dream}'—or you can be {age + 5} with a list of excuses. {location} is full of people waiting for 'the right time.' There is no right time. There is only right now. Build the life you won't need a vacation from.",
            f"Hey {name}, success in the {career} industry isn't about luck; it's about being the most prepared person in the room when opportunity knocks. You have a vision that most people are too scared to even write down. That alone puts you ahead. Stop looking for permission to be great. The version of you that achieves '{dream}' is already inside you—they are just waiting for you to start acting like them. Get to work.",
            f"The transition from where you are in {location} to where you want to be in 5 years is paved with 'boring' consistency. It's the early mornings, the extra courses, and the networking calls when you'd rather be sleeping. {name}, you aren't working this hard just to be 'average.' You are building a legacy. When you feel like quitting, remember that the pain of discipline is far lighter than the pain of regret."
        ]
        
        st.markdown(f"### ⚡ A Message for the Future {name}:")
        st.write(random.choice(motivations))
        st.caption("You have the plan. You have the tools. Now, you just need the courage to follow through.")

else:
    st.warning("👈 Please fill out your profile and your dream in the sidebar to generate your 5-year roadmap!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Built for the dreamers of Malaysia 🇲🇾 | Stay Disciplined. Stay Visionary.</p>", unsafe_allow_html=True)