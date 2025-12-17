import streamlit as st

st.set_page_config(
    page_title="5-Year Life Planner",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 5-Year Life Planner")
st.write("Answer a few questions and get a simple roadmap for the next 5 years.")

# Sidebar inputs
st.sidebar.header("About You")

name = st.sidebar.text_input("Your name")
age = st.sidebar.number_input("Your age", min_value=0, max_value=120, step=1)
career = st.sidebar.text_input("Current career / field")
location = st.sidebar.selectbox(
    "Where do you live?",
    ["Malaysia", "Singapore", "Other Asia", "Europe", "Middle East", "US / Canada", "Other"]
)
dream = st.sidebar.text_area(
    "What is your biggest dream?",
    placeholder="e.g. Become a senior data scientist, start a business, financial freedom..."
)

st.divider()

# Main logic
if name and career and dream:
    st.subheader(f"Hello {name} 👋")
    st.write(f"You are **{age}** years old, working in **{career}**, based in **{location}**.")

    st.divider()
    st.subheader("🎯 Your 5-Year Outlook")

    # Age-based guidance
    if age < 25:
        focus = "exploring, learning fast, and building strong foundations"
    elif age < 35:
        focus = "career acceleration, specialization, and financial growth"
    else:
        focus = "leadership, stability, and long-term impact"

    st.write(f"Based on your age, the next 5 years should focus on **{focus}**.")

    # 5-year plan
    st.subheader("🗺️ Suggested 5-Year Plan")

    st.markdown("""
    **Year 1–2**
    - Deepen skills related to your career
    - Build strong projects and practical experience
    - Improve communication and problem-solving skills

    **Year 3–4**
    - Move into more senior or specialized roles
    - Increase income and financial discipline
    - Start mentoring or leading small initiatives

    **Year 5**
    - Align your career directly with your dream
    - Aim for leadership, independence, or major life milestones
    - Reassess goals and design the next chapter
    """)

    st.divider()

    st.subheader("💭 Your Dream")
    st.write(f"**“{dream}”**")

    st.success(
        "If you stay consistent, disciplined, and curious, this dream is achievable within the next 5 years."
    )

    # Call to action
    if st.button("Generate Motivation"):
        st.balloons()
        st.write(
            f"🚀 {name}, small progress every day beats motivation. "
            "Focus on systems, not pressure."
        )

else:
    st.info("👈 Fill in all the details in the sidebar to generate your 5-year plan.")
