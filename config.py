from langchain_groq import ChatGroq
from langchain.tools import Tool
from utlis import stock_price_tool
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API Key for stock fetching
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = 'Gemma2-9b-It'

# Initialize LLM
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=MODEL_NAME)

# Define tools
stock_tool = Tool(
    name="Stock Price Fetcher",
    func=lambda symbol: stock_price_tool(symbol, ALPHA_VANTAGE_API_KEY),
    description="Fetches the latest stock price for a given stock symbol.",
)

calculator_tool = Tool(
    name="Calculator",
    func=lambda x: str(eval(x)),  
    description="A simple calculator for mathematical expressions.",
)

# Bind tools to LLM
tools = [stock_tool, calculator_tool]
llm_with_tools = llm.bind_tools(tools)
