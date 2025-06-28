import streamlit as st

st.set_page_config(
    page_title="SehatCheck App",
    page_icon="🩺"
)
st.title("SehatCheck 🩺")
st.write(

'''

SehatCheck adalah aplikasi diagnosis awal berbasis Python dan Streamlit yang membantu pengguna mengenali kemungkinan penyakit berdasarkan gejala yang dirasakan. Aplikasi ini menyediakan tiga metode analisis:

1. Rule-based, yaitu logika sederhana yang mengaitkan gejala dengan penyakit umum.

2. Model AI (Sklearn), menggunakan algoritma Naive Bayes untuk memprediksi penyakit dari kombinasi gejala.

3. Chatbot, asisten AI interaktif berbasis GPT yang dapat menjawab pertanyaan kesehatan secara real-time."

'''
)
st.info("Disclaimer: Ini bukan diagnosa medis resmi. Jika gejala berlanjut, segera hubungi tenaga medis profesional.")

st.sidebar.success("Select a page above.")