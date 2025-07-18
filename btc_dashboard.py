
# Bitcoin Risk İzleme Paneli – Streamlit Arayüzü
# Gerekenler: pip install streamlit pandas matplotlib

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Sahte veri oluşturma (gerçek veriler API ile entegre edilebilir)
base_date = datetime.date.today() - datetime.timedelta(days=30)
dates = [base_date + datetime.timedelta(days=i) for i in range(30)]
funding_rate = [0.01 + 0.002 * ((i % 7) - 3) for i in range(30)]  # dalgalı funding
price = [100000 + i*300 + (i % 5)*1000 for i in range(30)]  # artan BTC fiyatı
open_interest = [30e9 + (i % 10)*1e9 for i in range(30)]  # nominal OI

btc_price = pd.Series(price, index=dates)
funding = pd.Series(funding_rate, index=dates)
oi_nominal = pd.Series(open_interest, index=dates)
oi_normalized = oi_nominal / btc_price

# Risk analizi fonksiyonu
def risk_level(fund, oi_norm_delta, price_delta):
    if fund > 0.2 and oi_norm_delta < -0.01 and price_delta > 0:
        return "🔴 YÜKSEK RİSK (Long squeeze olasılığı)"
    elif fund > 0.1 and price_delta > 0:
        return "🔹 ORTA RİSK (Aşırı Isınma)"
    elif fund < 0 and oi_norm_delta > 0:
        return "🔶 SHORT SQUEEZE POTANSİYELİ"
    else:
        return "✅ DÜŞÜK RİSK"

# Yeni: Zaman Tabanlı Sinyal Skoru (15dk → 2h → 4h simülasyonu)
def time_based_score(idx):
    if idx < 4:
        return 50  # yeterli veri yoksa nötr
    short_term = price[idx] - price[idx - 1]
    mid_term = price[idx] - price[idx - 2]
    long_term = price[idx] - price[idx - 4]

    score = 50
    if short_term > 0: score += 5
    if mid_term > 0: score += 10
    if long_term > 0: score += 15
    if short_term < 0: score -= 5
    if mid_term < 0: score -= 10
    if long_term < 0: score -= 15
    return max(0, min(100, score))

# Risk seviyesi hesaplama
risk_signals = []
for i in range(1, len(dates)):
    fr = funding[dates[i]]
    oi_delta = (oi_normalized[dates[i]] - oi_normalized[dates[i-1]]) / oi_normalized[dates[i-1]]
    price_delta = (btc_price[dates[i]] - btc_price[dates[i-1]]) / btc_price[dates[i-1]]
    risk = risk_level(fr, oi_delta, price_delta)
    time_score = time_based_score(i)
    total_score = int((time_score + (100 if risk.startswith('✅') else 50)) / 2)
    risk_signals.append((dates[i], fr, oi_delta, price_delta, risk, time_score, total_score))

risk_df = pd.DataFrame(risk_signals, columns=[
    "Tarih", "Funding", "OI Değişim", "Fiyat Değişimi", "Risk Seviyesi", "Zaman Skoru", "Toplam Sinyal Skoru"])

# Streamlit arayüzü
st.set_page_config(page_title="Bitcoin Risk Paneli", layout="wide")
st.title("📈 Bitcoin Risk İzleme Paneli")
st.write("Funding Rate, Open Interest, Fiyat ve Zaman bazlı sinyal modellemesi")

# Grafikler
st.subheader("📊 Grafiksel Görünümler")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dates, btc_price, label="BTC Fiyatı ($)")
ax.plot(dates, oi_normalized * 1000, label="Normalize OI (x1000 BTC)")
ax.plot(dates, [f * 10000 for f in funding], label="Funding Rate (x10000)")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

# Tablo
st.subheader("📋 Günlük Risk Değerlendirmesi")
st.dataframe(risk_df.tail(10), use_container_width=True)

# Footer
st.caption("Veriler örneklemelidir. Gerçek API entegrasyonu uygulanabilir. Zaman bazlı sinyaller eklenmiştir.")
