# btc_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import fetch_metrics

st.set_page_config(page_title="Bitcoin Risk Paneli v3", layout="wide")
st.title("📈 Bitcoin Risk İzleme Paneli v3")
st.write("Yeni API ile 2 dakikada bir veri güncelleme ve çoklu metrik analizi")

# Veri çek
try:
    df = fetch_metrics()
    if df.empty:
        st.warning("Veri çekilemedi veya boş döndü. Lütfen daha sonra tekrar deneyin.")
    else:
        st.success(f"Güncellenme zamanı: {df['timestamp'].iloc[-1]}")
        st.dataframe(df.tail(10))

        # Basit görselleştirme
        st.line_chart(df.set_index("timestamp")[["price", "fundingRate", "oi"]])
except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
