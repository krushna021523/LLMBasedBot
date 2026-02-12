from fastapi import APIRouter, HTTPException
from openai import OpenAI
import os
import json
from backend.schema import ChatRequest, ChatResponse
from backend.services.weather import get_weather
from backend.services.service_functions import weather_function

router = APIRouter()

# Lazy initialization of OpenAI client
_client = None

def get_openai_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=api_key)
    return _client


async def handle_function_call(function_name: str, arguments: dict):
    """Handle function calls from OpenAI."""
    if function_name == "get_weather":
        city = arguments.get("city")
        if city:
            weather_data = await get_weather(city)
            return json.dumps(weather_data)
    return json.dumps({"error": "Unknown function"})

@router.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest) -> ChatResponse:
    """
    Chat completion endpoint with weather API integration via function calling.
    """
    try:
        client = get_openai_client()
        
        # Convert Pydantic models to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Make initial API call with function tools
        response = client.chat.completions.create(
            model=request.model,
            messages=openai_messages,
            temperature=request.temperature,
            tools=[weather_function],
            tool_choice="auto"  # Let the model decide when to use the function
        )
        
        message = response.choices[0].message
        assistant_message = message.content
        
        # Handle function calls if any
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # Call the function
                function_result = await handle_function_call(function_name, arguments)
                
                # Add function result to messages
                openai_messages.append({
                    "role": "assistant",
                    "content": assistant_message,
                    "tool_calls": message.tool_calls
                })
                openai_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_result
                })
            
            # Get final response from OpenAI with function results
            response = client.chat.completions.create(
                model=request.model,
                messages=openai_messages,
                temperature=request.temperature,
                tools=[weather_function]
            )
            assistant_message = response.choices[0].message.content
        
        return ChatResponse(
            message=assistant_message,
            role="assistant"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )