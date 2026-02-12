# Define weather function for OpenAI
weather_function = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a given city. Use this when users ask about weather conditions.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, e.g. 'London', 'New York', 'Tokyo'"
                }
            },
            "required": ["city"]
        }
    }
}