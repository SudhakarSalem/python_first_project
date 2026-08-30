from ollama import chat
from pymongo import MongoClient


# ============================================================
# 1. MongoDB CONNECTION
# ============================================================

uri = "mongodb+srv://sudhakarsalem_db_user:****@cluster0.teatimw.mongodb.net/"

client = MongoClient(uri)

db = client["test_db"]
customers = db["customers"]


# ============================================================
# 2. MONGODB TOOL
# ============================================================

def search_customers(
    city: str = "",
    min_purchase: int = 0,
    max_purchase: int = 999999999,
    min_age: int = 0,
    max_age: int = 999
) -> str:
    """
    Search customers in MongoDB.

    Args:
        city: Customer city. Leave empty for all cities.
        min_purchase: Minimum purchase amount.
        max_purchase: Maximum purchase amount.
        min_age: Minimum customer age.
        max_age: Maximum customer age.

    Returns:
        Matching customers as text.
    """

    query = {}

    # City filter
    if city:
        query["city"] = city

    # Purchase filter
    query["purchase"] = {
        "$gte": min_purchase,
        "$lte": max_purchase
    }

    # Age filter
    query["age"] = {
        "$gte": min_age,
        "$lte": max_age
    }

    results = list(
        customers.find(
            query,
            {
                "_id": 0,
                "name": 1,
                "city": 1,
                "age": 1,
                "purchase": 1
            }
        )
    )

    if not results:
        return "No customers found."

    return str(results)


# ============================================================
# 3. AVAILABLE TOOLS
# ============================================================

available_functions = {
    "search_customers": search_customers
}


# ============================================================
# 4. SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a helpful MongoDB database assistant.

You have access to a MongoDB customer database.

Use the search_customers tool whenever the user asks
about customer data.

Do not invent customer information.

After receiving MongoDB results, explain the answer
clearly and concisely.

Examples:

User:
Find customers from Chennai.

Action:
Use search_customers with city="Chennai".

User:
Who spent more than 50000?

Action:
Use search_customers with min_purchase=50000.

User:
Find Chennai customers who spent more than 60000.

Action:
Use search_customers with:
city="Chennai"
min_purchase=60000

Always use the database tool for database questions.
"""


# ============================================================
# 5. AGENT LOOP
# ============================================================

def run_agent(user_question):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    while True:

        response = chat(
            model="qwen3:4b",
            messages=messages,
            tools=[search_customers]
        )

        # Add the assistant response to conversation
        messages.append(response.message)

        # Did the model request a tool?
        if response.message.tool_calls:

            for tool_call in response.message.tool_calls:

                function_name = tool_call.function.name

                arguments = tool_call.function.arguments

                print("\n[Agent is using MongoDB...]")
                print("Tool:", function_name)
                print("Arguments:", arguments)

                function_to_call = available_functions.get(
                    function_name
                )

                if function_to_call:

                    result = function_to_call(
                        **arguments
                    )

                else:

                    result = "Unknown tool."

                print("[MongoDB result received]")

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": function_name,
                        "content": result
                    }
                )

        else:

            # No more tools needed.
            return response.message.content


# ============================================================
# 6. CHAT LOOP
# ============================================================

print("=" * 60)
print("MongoDB AI Agent")
print("Type 'exit' to quit.")
print("=" * 60)

while True:

    user_question = input("\nYou: ")

    if user_question.lower() == "exit":
        print("Goodbye!")
        break

    try:

        answer = run_agent(user_question)

        print("\nAgent:", answer)

    except Exception as e:

        print("\nError:", e)