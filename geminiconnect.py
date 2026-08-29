import os
from google import genai
from google.genai import types

# 1. Initialize the client
# The SDK automatically pulls the GEMINI_API_KEY environment variable.
client = genai.Client()

# 2. Define your prompts
system_instruction = "You are a helpful culinary assistant. Always respond like a 1920s pirate."
user_message = "How do I make a perfect cup of coffee?"

# 3. Call the model with the system instruction configuration
response = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents=user_message,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        # You can add optional parameters here like:
        temperature=0.7,
    ),
)

# 4. Print the result
print(response.text)
