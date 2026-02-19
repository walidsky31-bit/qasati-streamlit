import streamlit as st

st.title("📚 قصتي")
st.write("تطبيق توليد قصص أطفال")

name = st.text_input("اسم الطفل")
st.write(f"مرحباً {name}!")
