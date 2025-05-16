import json
import os

from langchain_core.messages import HumanMessage
import requests
from pymongo import MongoClient
from langchain_google_genai import ChatGoogleGenerativeAI
from flask import Flask, jsonify, request, send_file, send_from_directory, make_response

# 🔥 FILL THIS OUT FIRST! 🔥
# Get your Gemini API key by:
# - Selecting "Add Gemini API" in the "Firebase Studio" panel in the sidebar
# - Or by visiting https://g.co/ai/idxGetGeminiKey
os.environ["GOOGLE_API_KEY"] = "AIzaSyCxFh8g7h4kyvxSzUYmMsfY9tGFU6f8JNs"; 

app = Flask(__name__)

# MongoDB connection details
MONGO_URI = "mongodb://root:9a5e7628-f513-4dda-99ee-785a19a753a3@146.190.110.16:27017/admin?retryWrites=true&loadBalanced=false&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"

def mongoTool():
    client = MongoClient(MONGO_URI)
    db = client["p2p_trading"]
    orders_collection = db["orders"]
    orders_data = list(orders_collection.find({}, {"_id": 1, "type": 1, "amount": 1, "price": 1, "total_price": 1, "currency": 1, "status": 1}))
    # Convert ObjectId to string for JSON serialization
    print(orders_data)
    for order in orders_data:
        order["_id"] = str(order["_id"])
    return orders_data


@app.route("/")
def index():
    return send_file('web/index.html')


@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = ChatGoogleGenerativeAI(model=req_body.get("model"))
            message = HumanMessage(
                # Use a human message to start the conversation.
                content=content
            )
            response = model.stream([message])
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.content })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })


@app.route("/chatbot", methods=["POST"])
def chatbot_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            message = req_body.get("message", "").lower()
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash") # Using Gemini Pro for the chatbot

            # Check if the message relates to orders
            if "order" in message or "orders" in message:
                # replace this code with a reall call to function mongoTool() and print the results from the function
                orders_data = mongoTool()
                # Craft a prompt for the LLM including the order data
                prompt = f"The user is asking about their orders. Here is their order data: {json.dumps(orders_data)}. Please provide a helpful summary of their orders based on the user's question: '{message}'"
            else:
                prompt = message

            # Use LLM to get response
            response = llm.invoke(prompt) # Using invoke for chat models
            response_text = response.content
            return jsonify({ "response": str(response_text) })
        except Exception as e:
            return jsonify({ "error": str(e) })

            
@app.route("/google_chat", methods=["POST"])
def google_chat_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            message = req_body.get("message")

            # Prepare the payload for the internal API call
            payload = {
                "app_name": "google_search_agent",
                "user_id": "u_123",  # Replace with actual user ID if available
                "session_id": "s_123",  # Replace with actual session ID if available
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}]
                }
            }
            internal_api_url = "http://0.0.0.0:8080/run"
            response = requests.post(internal_api_url, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": str(e)})

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))
