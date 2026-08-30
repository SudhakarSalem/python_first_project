import os
from google import genai
from google.genai import types

from pymongo import MongoClient


import urllib.parse
from pymongo import MongoClient

# Encode username and password safely



uri = "mongodb+srv://sudhakarsalem_db_user:password@cluster0.teatimw.mongodb.net/"

client = MongoClient(uri)

db = client["test_db"]
student_collection = db["student"]

count = student_collection.count_documents({})


collection = db["student"]

# 2. Initialize Gemini Client
ai_client = genai.Client()

# 3. Define the Natural Language Prompt

# 4. Construct a System Instruction to force JSON MongoDB query output
students = student_collection.find(
    {"grade": "B"},
    {"_id": 0}
)

# Display students
for student in students:
    print(student)

# Close connection
client.close()
# 5. Call Gemini
# 6. Parse the LLM response and Query MongoDB