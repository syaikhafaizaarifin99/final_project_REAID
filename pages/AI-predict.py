import streamlit as st
import pandas as pd
import random
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from openai import OpenAI
import os

# === Data gejala dan kemungkinan penyakit (Rule-based) ===
gejala_list = [
    "Demam", "Batuk", "Pusing", "Mual", "Sakit tenggorokan",
    "Sesak napas", "Pilek", "Nyeri otot", "Lemas"
]

penyakit_map = {
    "Demam": ["Flu", "Demam Berdarah", "COVID-19"],
    "Batuk": ["Flu", "Bronkitis", "COVID-19"],
    "Pusing": ["Migrain", "Vertigo", "Tekanan darah rendah"],
    "Mual": ["Keracunan makanan", "Maag", "Infeksi usus"],
    "Sakit tenggorokan": ["Radang tenggorokan", "Flu", "COVID-19"],
    "Sesak napas": ["Asma", "COVID-19", "Pneumonia"],
    "Pilek": ["Flu", "Alergi", "COVID-19"],
    "Nyeri otot": ["Flu", "Tifus", "Kelelahan otot"],
    "Lemas": ["Anemia", "Kurang tidur", "Tifus"]
}

saran_map = {
    "Flu": "Perbanyak istirahat, minum air hangat, dan konsumsi vitamin C.",
    "Demam Berdarah": "Segera ke dokter. Cek trombosit secara berkala.",
    "COVID-19": "Lakukan tes antigen/PCR. Isolasi mandiri dan pakai masker.",
    "Bronkitis": "Konsultasi ke dokter, hindari asap rokok.",
    "Migrain": "Istirahat di ruangan gelap dan hindari suara bising.",
    "Vertigo": "Duduk atau berbaring hingga rasa pusing reda.",
    "Keracunan makanan": "Minum oralit dan hindari makanan mencurigakan.",
    "Maag": "Hindari makanan pedas dan asam. Makan teratur.",
    "Infeksi usus": "Minum air bersih dan jaga kebersihan makanan.",
    "Radang tenggorokan": "Kumur air garam dan banyak minum.",
    "Asma": "Gunakan inhaler jika diperlukan dan hindari pemicu.",
    "Pneumonia": "Segera konsultasi ke rumah sakit.",
    "Alergi": "Hindari alergen dan konsumsi antihistamin bila perlu.",
    "Tifus": "Periksa ke dokter dan istirahat total.",
    "Anemia": "Konsumsi makanan tinggi zat besi.",
    "Kurang tidur": "Tidur cukup minimal 7–8 jam."
}

# === Sklearn AI Model ===
X_data = ["demam batuk pilek", "pusing mual", "sakit tenggorokan batuk", "sesak napas batuk demam"]
y_data = ["Flu", "Maag", "Radang Tenggorokan", "COVID-19"]
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_data)
model = MultinomialNB()
model.fit(X_train, y_data)

st.title("SehatCheck - Cek Gejala")
st.write("Masukkan gejala yang kamu rasakan dan dapatkan kemungkinan penyakit beserta saran tindakan awal.")

st.subheader("Pilih Metode Diagnosa")
metode = st.radio("Metode yang ingin digunakan:", ["Rule-based", "AI Model (sklearn)"])

# === Input gejala ===
selected_gejala = st.multiselect("Pilih gejala kamu:", gejala_list)

# === Tombol cek hanya muncul untuk rule-based & AI model ===
if not selected_gejala:
    st.warning("Pilih minimal satu gejala.")
else:
    if metode == "Rule-based":
        kemungkinan_penyakit = []
        for gejala in selected_gejala:
            kemungkinan_penyakit.extend(penyakit_map.get(gejala, []))
        hasil = list(set(kemungkinan_penyakit))
        st.subheader("Kemungkinan Penyakit (Rule-based):")
        for penyakit in hasil:
            st.markdown(f"- **{penyakit}**")
        st.subheader("Saran Tindakan Awal:")
        for penyakit in hasil:
            saran = saran_map.get(penyakit, "Konsultasikan lebih lanjut dengan dokter.")
            st.markdown(f"**{penyakit}**: {saran}")

    elif metode == "AI Model (sklearn)":
        input_user = " ".join(selected_gejala).lower()
        X_test = vectorizer.transform([input_user])
        prediction = model.predict(X_test)
        st.subheader("Prediksi AI (sklearn):")
        st.write(f"⚠️ Kemungkinan besar: **{prediction[0]}**")
        saran = saran_map.get(prediction[0], "Konsultasikan lebih lanjut dengan dokter.")
        st.write(f"💡 Saran: {saran}")

    st.info("Disclaimer: Ini bukan diagnosa medis resmi. Jika gejala berlanjut, segera hubungi tenaga medis profesional.")
