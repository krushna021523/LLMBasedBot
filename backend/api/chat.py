from fastapi import APIRouter, HTTPException
import requests
import json
from backend.schema import ChatRequest, ChatResponse
from backend.services.weather import get_weather

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"


async def handle_function_call(function_name: str, arguments: dict):
    if function_name == "get_weather":
        city = arguments.get("city")
        if city:
            weather_data = await get_weather(city)
            return json.dumps(weather_data)

    return json.dumps({"error": "Unknown function"})


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest) -> ChatResponse:
    try:

        # Convert messages into Ollama format
        ollama_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        # Add system instruction to guide tool usage
        ollama_messages.insert(0, {
            "role": "system",
            "content": """
You are an assistant.
If the user asks about weather, respond ONLY in JSON format like:
{
  "function_call": "get_weather",
  "arguments": {"city": "CityName"}
}
Otherwise respond normally.
"""
        })

        # First call to Llama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": ollama_messages,
                "stream": False,
                
            }
        )

        data = response.json()
        assistant_message = data["message"]["content"]

        # Try to detect function call
        try:
            parsed = json.loads(assistant_message)

            if "function_call" in parsed:
                function_name = parsed["function_call"]
                arguments = parsed.get("arguments", {})

                function_result = await handle_function_call(function_name, arguments)

                # Send function result back to Llama for final answer
                ollama_messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                ollama_messages.append({
                    "role": "user",
                    "content": f"Function result: {function_result}. Give final response to user."
                })

                final_response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL_NAME,
                        "messages": ollama_messages,
                        "stream": False
                    }
                )

                final_data = final_response.json()
                assistant_message = final_data["message"]["content"]

        except json.JSONDecodeError:
            pass

        return ChatResponse(
            message=assistant_message,
            role="assistant"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )