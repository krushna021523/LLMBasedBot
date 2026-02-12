# LLMBasedBot Chatbot Application

A full-stack chatbot application with a FastAPI backend and Streamlit frontend, powered by Llama3's chat completion API.

## Features

- 🤖 Interactive chat interface built with Streamlit
- 🚀 FastAPI backend with Llama3 integration
- ⚙️ Configurable model selection and temperature settings
- 💬 Chat history maintained throughout the session
- 🔄 Real-time API communication
- 🌦️ Weather API integration via Llama3 function

## Project Structure

```
agentic-bot/
├── backend/
│   ├── api/
│   │   ├── __init__.py           # Router registration with /agent prefix
│   │   └── chat.py               # Chat API endpoint with function calling
│   ├── services/
│   │   ├── __init__.py
│   │   ├── service_functions.py # Weather function definition for OpenAI
│   │   └── weather.py            # Weather API integration
│   ├── main.py                   # FastAPI app with ping endpoint
│   └── schema.py                 # Pydantic models for validation
├── frontend/
│   └── app.py                    # Streamlit frontend application
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup Instructions
### Ensure You are using Python 3.11 ( preferably 3.11.9)
```python --version
```
### 1. Create a virtual environment
```powershell
  python -m venv krish_venv
  ```
### 2. Activate the virtual environment(For Windows)
```
./krish_venv/Scripts/Activate.ps1 
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root and add your API keys:

```
OPENAI_API_KEY=your_actual_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

- **OpenAI API Key**: Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Weather API Key**: Get a free API key from [OpenWeatherMap](https://openweathermap.org/api) (optional, only needed for weather functionality)

### 5. Run the Backend

In one terminal window, from the project root:

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Or if running from the backend directory:

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### 6. Run the Frontend

In another terminal window:

```bash
streamlit run frontend/app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

## API Endpoints

### GET `/`

Ping endpoint to check if the API is running.

**Response:**
```json
{
  "message": "Agentic Chatbot API is running"
}
```

### POST `/agent/chat`

Chat completion endpoint that processes user queries using OpenAI with function calling support.

**Request Body:**
```json
{
    "model": MODEL_NAME,
    "messages": ollama_messages,
    "stream": false
```

**Response:**
```json
{
  "message": "Hello! How can I assist you today?",
  "role": "assistant"
}
```

**Note**: This endpoint supports OpenAI function calling. The chatbot can automatically call the weather function when users ask about weather conditions.

## Usage

1. Make sure both the backend and frontend are running
2. Open the Streamlit app in your browser
3. Type your message in the chat input
4. The chatbot will respond using Llama3
5. Use the sidebar to configure model settings and clear chat history

## Notes

- The backend uses CORS middleware to allow requests from the Streamlit frontend
- Chat history is maintained in the Streamlit session state
- The API requires a valid OpenAI API key to function
- Weather functionality requires a `WEATHER_API_KEY` in the `.env` file (optional)
- Default model is `llam3` but you can switch to other models in the sidebar after adding them in the frontend app.py file.
- The chatbot supports function calling for weather queries via Llama3

## Troubleshooting

- **API Connection Error**: Make sure the FastAPI backend is running on port 8000
- **Llama3 API Error**: Verify your local Llama service responds at http://localhost:11434/api/chat
- **Weather Function Error**: If weather queries fail, ensure `WEATHER_API_KEY` is set in the `.env` file
- **Import Errors**: Ensure all dependencies are installed using `pip install -r requirements.txt`

