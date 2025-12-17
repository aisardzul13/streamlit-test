import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Data Explorer/Discovery", layout="wide")

st.title("📊 CSV Data Explorer")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📈 Summary Statistics")
    st.write(df.describe(include="all"))

    st.subheader("🎯 Filter Data")

    col = st.selectbox("Select a column to filter", df.columns)

    if pd.api.types.is_numeric_dtype(df[col]):
        min_val, max_val = float(df[col].min()), float(df[col].max())
        selected_range = st.slider(
            "Select range",
            min_val,
            max_val,
            (min_val, max_val)
        )
        filtered_df = df[
            (df[col] >= selected_range[0]) &
            (df[col] <= selected_range[1])
        ]
    else:
        unique_vals = df[col].astype(str).unique()
        selected_vals = st.multiselect(
            "Select values",
            unique_vals,
            default=unique_vals
        )
        filtered_df = df[df[col].astype(str).isin(selected_vals)]

    st.subheader("📊 Filtered Data")
    st.dataframe(filtered_df)

    st.subheader("📉 Chart")
    numeric_cols = filtered_df.select_dtypes(include="number").columns

    if len(numeric_cols) >= 1:
        st.line_chart(filtered_df[numeric_cols])
    else:
        st.info("No numeric columns available for charting.")
else:
    st.info("👆 Upload a CSV file to begin.")
