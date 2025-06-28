import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

st.title("Chatbot AI Dokter")
st.markdown("Masukkan keluhan atau pertanyaan di bawah ini untuk mendapatkan saran awal.")
st.divider()

# Inisialisasi riwayat chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "Kamu adalah asisten medis yang memberikan saran awal (bukan diagnosa resmi)."}
    ]

# Tampilkan seluruh riwayat chat sebelumnya
for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input dari pengguna
user_input = st.chat_input("Tanyakan sesuatu...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Sedang menjawab..."):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history
            )
            reply = response.choices[0].message.content
            st.chat_message("assistant").markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghubungi API OpenAI: {e}")

st.info("Disclaimer: Ini bukan diagnosa medis resmi. Jika gejala berlanjut, segera hubungi tenaga medis profesional.")
