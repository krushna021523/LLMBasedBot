import streamlit as st
import requests
import json
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="Agentic Chatbot",
    page_icon="🤖",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000/agent/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_available" not in st.session_state:
    st.session_state.api_available = False

# Check API connection on startup
if "api_checked" not in st.session_state:
    try:
        ping_response = requests.get("http://localhost:8000/", timeout=2)
        if ping_response.status_code == 200:
            st.session_state.api_available = True
    except:
        st.session_state.api_available = False
    st.session_state.api_checked = True

# Sidebar for configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    api_url = st.text_input(
        "API URL",
        value=API_URL,
        help="URL of the FastAPI backend"
    )
    
    model = st.selectbox(
        "Model",
        options=["llama3"],
        index=0
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        key="temperature"
    )
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("🤖 Agentic Chatbot")
st.markdown("---")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # First, check if API is still available before making chat request
                try:
                    ping_response = requests.get("http://localhost:8000/", timeout=2)
                    if ping_response.status_code != 200:
                        st.session_state.api_available = False
                        st.error("❌ API is not responding correctly")
                        st.stop()
                except:
                    st.session_state.api_available = False
                    st.error("❌ Cannot connect to the API. Make sure the FastAPI backend is running on port 8000.")
                    st.stop()
                
                # Prepare messages for API
                api_messages = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages
                ]
                
                # Make API request
                payload = {
                    "messages": api_messages,
                    "model": model,
                    #"temperature": st.session_state.temperature
                }
                
                response = requests.post(
                    api_url,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data["message"]
                    st.markdown(assistant_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    st.session_state.api_available = True
                else:
                    error_msg = f"❌ API Error: {response.status_code}\n{response.text}"
                    st.error(error_msg)
                    st.session_state.api_available = False
                    
            except requests.exceptions.ConnectionError:
                error_msg = "❌ Cannot connect to the API. Make sure the FastAPI backend is running on port 8000."
                st.error(error_msg)
                st.session_state.api_available = False
            except requests.exceptions.Timeout:
                error_msg = "❌ Request timeout. The API took too long to respond."
                st.error(error_msg)
                st.session_state.api_available = False
            except Exception as e:
                error_msg = f"❌ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.api_available = False



