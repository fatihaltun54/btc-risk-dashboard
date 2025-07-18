# Bitcoin Risk İzleme Paneli v3 – CoinGlass API Entegrasyonu ile
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import get_funding_data

st.set_page_config(page_title="Bitcoin Risk Paneli v3", layout="wide")
st.title("📈 Bitcoin Risk İzleme Paneli v3")
st.write("Yeni API ile 2 dakikada bir veri güncelleme ve çoklu metrik analizi")

data = get_funding_data()

if data is None or len(data) == 0:
    st.error("Veri çekilemedi veya boş döndü. Lütfen daha sonra tekrar deneyin.")
else:
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["fundingTime"], unit="ms")
    df.set_index("time", inplace=True)

    st.subheader("📊 Funding Rate ve BTC Fiyatı")
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(df.index, df["markPrice"].astype(float), label="BTC Fiyatı", color="blue")
    ax2 = ax1.twinx()
    ax2.plot(df.index, df["fundingRate"].astype(float), label="Funding Rate", color="orange")
    ax1.set_ylabel("BTC Fiyatı ($)")
    ax2.set_ylabel("Funding Rate")
    ax1.grid(True)
    fig.tight_layout()
    st.pyplot(fig)

    st.subheader("📋 Ham Veri")
    st.dataframe(df[["fundingRate", "markPrice"]])