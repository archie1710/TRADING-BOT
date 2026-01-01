 Simplified Binance Futures Trading Bot

A robust Python-based trading bot designed for the **Binance Futures Testnet (USDT-M)**. This tool allows users to execute multiple order types with full logging, error handling, and input validation.

---


- **Full Futures Testnet Support:** Explicitly configured for `testnet.binancefuture.com`.
- **Order Types:**
  - `MARKET`: Instant execution at market price.
  - `LIMIT`: Traditional Good-Till-Canceled (GTC) orders.
  - `STOP-LIMIT` (Bonus): Advanced trigger logic for risk management (`STOP` type for Futures).
- **Security First:** Designed to load API credentials via environment variables to prevent accidental exposure.
- **Robust Logging:** Every API request, JSON response, and error is recorded in `trading_bot.log`.
- **Validation Layer:** Prevents script crashes by validating all CLI inputs (Quantity, Price, Side).

---

## 🛠 Tech Stack
- **Language:** Python 3.x
- **API Library:** `python-binance`
- **Logging:** Python Standard `logging` library

---

## Getting Started

### 1. Prerequisites
- Python 3.8+
- A Binance Testnet Account ([Register here](https://testnet.binancefuture.com/))

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/binance-trading-bot.git](https://github.com/YOUR_USERNAME/binance-trading-bot.git)
cd binance-trading-bot

# Install dependencies
pip install python-binance
