import streamlit as st

# Page config
st.set_page_config(
    page_title="Interactive Streamlit App",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 My Interactive Streamlit App")
st.write("A simple app to demonstrate Streamlit features.")

# Sidebar
st.sidebar.header("User Info")
name = st.sidebar.text_input("Your name")
age = st.sidebar.number_input("Your age", min_value=0, max_value=120, step=1)

st.divider()

# Main content
if name:
    st.subheader(f"Hello, {name} 👋")

    if age < 18:
        st.info("You are under 18. Keep learning and exploring!")
    elif age < 30:
        st.success("Great age to build skills and your career 🚀")
    else:
        st.warning("Experience is your superpower 💡")

    # Button interaction
    if st.button("Analyze profile"):
        st.write("Analyzing your profile...")

        progress = st.progress(0)
        for i in range(100):
            progress.progress(i + 1)

        st.success("Analysis complete!")

        st.metric(label="Learning Score", value="85%", delta="+5%")

else:
    st.write("👈 Enter your details in the sidebar to get started.")
