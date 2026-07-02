import streamlit as st
import pandas as pd

df = pd.read_csv(
    "hospital_patients.csv"
)

st.title(
"Hospital Emergency Room Analytics"
)

st.metric(
"Total Patients",
len(df)
)

st.metric(
    "Critical Patients",
    len(df[df["Priority_Category"]
           =="Critical"])
)

st.dataframe(df)

st.bar_chart(
df["Priority_Category"]
.value_counts()
)