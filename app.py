import pandas as pd
import streamlit as st

st.title("Customer Purchasing Behaiour Dataset Analysis")

st.subheader("Full Dataset")
df = pd.read_csv("Customer-Purchasing-Behaviors.csv")
st.write(df)

st.subheader("First Five Rows")
st.write(df.head())

st.subheader("Last Five Rows")
st.write(df.tail())
