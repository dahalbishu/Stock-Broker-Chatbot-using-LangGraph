

import streamlit as st
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from config import llm, tools, llm_with_tools
from utlis import stock_transaction, chatbot, route_tools, State

def create_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", lambda state: chatbot(state, llm_with_tools))
    
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_node("stock_transaction", lambda state: stock_transaction(state, llm))
    
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", route_tools)
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge("stock_transaction", END)
    
    return graph_builder.compile()

def main():
    st.title("Stock Broker Chatbot")
    st.markdown(
        """
        Welcome to the **Stock Broker Chatbot**! 📈💬

        This chatbot helps you make informed decisions in the stock market. You can check the latest stock prices, and if you want to buy or sell shares, simply use the keywords 'buy' or 'sell'.

        The chatbot will calculate the total price based on the current stock value and provide instant responses!

        Enter your query in the chatbox below and get started!
        """
    )

    if "graph" not in st.session_state:
        st.session_state.graph = create_graph()

    user_input = st.chat_input("Ask me about stocks...")
    if user_input:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        initial_state = {
            "messages": [
                {"role": "system", "content": "You are a stock broker. You help people calculate their stock balance."},
                {"role": "user", "content": user_input}
            ]
        }
        
        events = st.session_state.graph.stream(initial_state, stream_mode="values")
        
        last_event = None
        for event in events:
            last_event = event
        
        if last_event:
            bot_response = getattr(last_event["messages"][-1], "content", "").strip()
            if not bot_response:
                bot_response = "I'm not supposed to answer this."
            
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"```{bot_response}```")

if __name__ == "__main__":
    main()