# Stock Broker Chatbot

Welcome to the Stock Broker Chatbot! 📈💬

This chatbot helps you make informed decisions in the stock market. You can check the latest stock prices, and if you want to buy or sell shares, simply use the keywords **'buy'** or **'sell'**.

The chatbot will calculate the total price based on the current stock value and provide instant responses!

## Installation

1. Setup:

   ```bash
   conda create --name myenv python=3.10.16 -y
   conda activate myenv
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys in a `.env` file:
   ```env
   ALPHA_VANTAGE_API_KEY='your_alpha_vantage_api'
   GROQ_API_KEY='your_groq_api'
   ```

4. Run the application:
   ```bash
   streamlit run main.py
   ```

## Outputs

- Some snapshots of results and language graphs are provided in the `outputs` directory.

Enjoy trading with the Stock Broker Chatbot! 🚀

**Note:** Due to the unavailability of transaction APIs, we have implemented simple simulated transactions. In the future, if such APIs become available, we could integrate them to link with a trading account.
