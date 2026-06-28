# 🌍 Country Information Agent

A Streamlit-based AI agent that answers questions about countries and fetches real-time data using the [REST Countries API](https://restcountries.com/). It uses OpenRouter to interface with LLMs and dynamically call tools to provide accurate and up-to-date information.

## 🚀 Features

- **Interactive Chat Interface**: A clean and easy-to-use chat UI powered by Streamlit.
- **Tool Calling**: The agent can autonomously decide to fetch specific country information (capital, region, population, currencies, languages) using the `get_country_info` tool.
- **LLM Integration**: Configured to use OpenRouter to process queries using models like `google/gemma-4-31b-it`.

## 🛠️ Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory and add your OpenRouter API key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

### 3. Run the Application
Start the Streamlit app:
```bash
streamlit run app.py
```
The app will open in your browser, and you can start asking questions about any country!
