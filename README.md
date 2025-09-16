# 📊 Crypto Dashboard with Chat Assistant

It provides a crypto dashboard with live data from [CoinGecko API](https://www.coingecko.com/en/api) and a **rule-based chat assistant** to answer user queries.

---

## 🚀 Features

### 🔹 Backend (Django)
- Fetches and stores top 10 cryptocurrencies with their prices, volume, and % changes.
- Fetches 30 days of historical price data for selected coins.
- Provides REST API endpoints:
  - `/api/top-coins/` → Get top N coins.
  - `/api/coin-history/<coin_id>/` → Get historical prices for last 30 days.
  - `/api/qa/?q=<query>` → Rule-based Q&A endpoint (e.g. “What is the price of Bitcoin?”).

### 🔹 Frontend (React)
- Dashboard displaying:
  - Table of top 10 coins (price, volume, % change).
  - Line chart of selected coin’s historical trend.
- Chat assistant panel where users can type natural queries.
- Integrates directly with Django backend APIs.

---

## 🛠️ Tech Stack

- **Backend:** Django REST Framework, CoinGecko API
- **Frontend:** React, Axios, Chart.js / Recharts
- **Database:** SQLite (default, can be swapped with Postgres/MySQL)
- **Extras:** Caching with Django cache framework

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/MohammadUsmanJan/crypto-dashboard.git
cd crypto-dashboard
