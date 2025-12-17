import streamlit as st

st.title("My First Streamlit App 🚀")

name = st.text_input("What is your name?")
age = st.number_input("How old are you?", min_value=0, max_value=120)

if name:
    st.write(f"Hello **{name}**! You are **{age}** years old.")
