import requests
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages

# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Function to fetch stock price
def fetch_stock_price(symbol: str, api_key: str):
    """Fetch the latest stock price for a given symbol from Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        time_series = data.get("Time Series (1min)")
        if not time_series:
            return None

        latest_time = list(time_series.keys())[0]
        latest_price = float(time_series[latest_time]["1. open"])
        
        return {"symbol": symbol, "time": latest_time, "price": latest_price}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to return stock price
def stock_price_tool(symbol: str, api_key: str) -> str:
    """Fetch the stock price."""
    result = fetch_stock_price(symbol, api_key)
    
    if not result or "error" in result:
        return f"Error fetching stock price: {result['error']}"
    return f"Stock: {result['symbol']}, Time: {result['time']}, Price: ${result['price']}"

# Chatbot function
def chatbot(state: State, llm_with_tools):
    """Process user messages with LLM and tools."""
    messages = state.get("messages", [])  
    return {"messages": messages + [llm_with_tools.invoke(messages)]}  

# Function to handle stock transactions
def stock_transaction(state: State, llm):
    messages = state.get("messages", [])
    last_message = messages[-1].content.lower()
    transaction_type = messages[1].content.lower()

    total_price = float(llm.invoke(f"Return only total price: nothing more, no any symbol or anything, just number \n input: {last_message}").content)

    brokerage_per = 0.05
    total_brokerage_fee = total_price * brokerage_per

    if "buy" in transaction_type:
        response = (
            f"Buy Transaction:\n"
            f"Total before charges: ${total_price}\n"
            f"Brokerage Fee (0.05%): ${total_brokerage_fee:.2f}\n"
            f"Final Amount: ${total_price + total_brokerage_fee:.2f}\n"
            f"Transaction of share is done successfully"
        )
    elif "sell" in transaction_type:
        response = (
            f"Sell Transaction:\n"
            f"Total before charges: ${total_price}\n"
            f"Brokerage Fee (0.05%): ${total_brokerage_fee:.2f}\n"
            f"Final Amount: ${total_price - total_brokerage_fee:.2f}\n"
            f"Transaction of share is done successfully"
        )
    else:
        response = "Transaction type not recognized."

    return {"messages": messages + [response]}


# Function to route tools or transactions
def route_tools(state: State):
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if messages and hasattr(messages[1], "content"):
        user_message = messages[1].content.lower()
    else:
        user_message = ""

    if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
        return "tools"
    
    elif "buy" in user_message or "sell" in user_message:
        return "stock_transaction"
    
    return "END"
