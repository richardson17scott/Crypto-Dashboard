# 🌐 Multi-Chain Crypto Portfolio Dashboard

An interactive, high-precision crypto wallet valuation dashboard built with Python, Streamlit, and Web3 data APIs. It automatically scans a given public EVM wallet address across multiple major blockchains, detects any token holding down to a microscopic scale (e.g., `0.00001`), fetches live fiat market values in Indian Rupees (INR) sequentially, and visualizes asset allocation instantly.

---

## 🚀 Key Features

- **Dynamic Asset Discovery:** Queries advanced multi-chain indexers to instantly scan all active token records within a wallet without needing a static, hardcoded list of tokens.
- **Multi-Chain Coverage:** Support for major EVM networks concurrently, including **Ethereum, Polygon, BNB Chain, Arbitrum, Base, and Avalanche**.
- **Micro-Holding Support:** Preserves exact fractional balances (e.g., `0.00001`) natively through floating-point precision parsing.
- **Live Fiat Valuation:** Fetches live quotes directly in **INR** using real-time tracking markets.
- **Rich Interactive Visualizations:** Built-in allocation analysis charts using interactive Plotly pie visualizations alongside tabular summary panels.

---

## 🛠️ Architecture Design

The app splits responsibility across three specialized modules:

1. **`blockchain.py` (The Scanner):** Interfaces with Ankr's Multi-Chain advanced indexed RPC gateway to pull complete account state vectors across multiple networks simultaneously.
2. **`api.py` (The Translator):** Connects to the CoinMarketCap developer API to parse real-time market price quotes under strict security headers.
3. **`app.py` (The UI Engine):** A wide-layout Streamlit application that links inputs, runs multi-tier sequential mapping computations, aggregates net worth evaluation mathematics, and renders the frontend visualizations.

---

## 📦 Project Structure

```text
├── app.py           # Streamlit user interface, data frame parsing, and charts
├── api.py           # CoinMarketCap individual live asset price quote driver
├── blockchain.py    # Ankr multi-chain advanced accounting indexer client
├── requirements.txt # Python dependency configurations
└── api_key.txt      # Private CoinMarketCap API Key credential (User Generated)
```

## ⚙️ Installation & Setup
1. Clone the Repository
Ensure you have Git installed, then initialize your folder environment:
```Bash
git clone https://github.com/richardson17scott/Crypto-Dashboard.git
cd Crypto-Dashboard
```
2. Configure Dependencies
Install the required packages using pip:
```Bash
pip install -r requirements.txt
```
3. Add Your API Credentials
Create a plain-text file named exactly .env in the root folder directory and paste your private CoinMarketCap developer API Key inside:
```Plaintext
CMC_API_KEY="your_coinmarketcap_api_key_here"
Ankr_api_key="your_ankr_api_key_here"
```
⚠️ Security Warning: Never check your api_key.txt file into git control. Ensure your local .gitignore includes api_key.txt to keep your credentials safe.

🖥️ Running the App
Launch the local development web server using Streamlit:
```Bash
streamlit run app.py
```
Once running, open your web browser to the default local address (usually http://localhost:8501), paste any public EVM wallet address (e.g., 0xfA89...), and click "Calculate Live Portfolio Net Worth".

## 🔒 License
This repository is open-source and available under the MIT License. Feel free to modify and build upon it!