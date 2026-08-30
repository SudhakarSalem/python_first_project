import os
from google import genai
from google.genai import types

from pymongo import MongoClient


import urllib.parse
from pymongo import MongoClient

# Encode username and password safely



uri = "mongodb+srv://sudhakarsalem_db_user:1ztM8NXKQ4juXEKm@cluster0.teatimw.mongodb.net/"

client = MongoClient(uri)

db = client["test_db"]
customers = db["customers"]

customers.delete_many({})

sample_customers = [
    {
        "name": "Ravi",
        "city": "Chennai",
        "age": 35,
        "purchase": 75000
    },
    {
        "name": "Kumar",
        "city": "Chennai",
        "age": 42,
        "purchase": 62000
    },
    {
        "name": "Arun",
        "city": "Bangalore",
        "age": 31,
        "purchase": 45000
    },
    {
        "name": "Priya",
        "city": "Chennai",
        "age": 29,
        "purchase": 90000
    },
    {
        "name": "Meena",
        "city": "Mumbai",
        "age": 38,
        "purchase": 55000
    }
]

customers.insert_many(sample_customers)

print("Database created successfully!")
print(f"Inserted {customers.count_documents({})} customers.")
