from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Simple built-in food review knowledge base.
# You can replace/extend this with a database or an AI API later.
FOOD_REVIEWS = {
    "pizza": {
        "rating": 4.5,
        "review": "Cheesy, crispy at the edges, and filling. A good choice when you want a comfort-food meal.",
        "tips": "Try it with extra cheese and a spicy dip."
    },
    "burger": {
        "rating": 4.2,
        "review": "Juicy patty, soft bun, and a satisfying combination of sauces and vegetables.",
        "tips": "Ask for a freshly grilled patty and pair it with fries."
    },
    "biryani": {
        "rating": 4.7,
        "review": "Fragrant rice, flavorful spices, and tender pieces make it a popular hearty meal.",
        "tips": "Raita and a little salna can balance the spice."
    },
    "dosa": {
        "rating": 4.6,
        "review": "Crispy outside, soft inside, and especially good with fresh chutney and sambar.",
        "tips": "Masala dosa is a great option if you want a more filling version."
    },
    "noodles": {
        "rating": 4.1,
        "review": "Quick, tasty, and easy to customize with vegetables, egg, or protein.",
        "tips": "Choose a less-oily preparation if you prefer a lighter meal."
    },
    "ice cream": {
        "rating": 4.4,
        "review": "Cold, creamy, and refreshing, with plenty of flavor options.",
        "tips": "Try a flavor that contrasts with your main meal."
    }
}

def find_food(message):
    text = message.lower()
    for food in FOOD_REVIEWS:
        if food in text:
            return food
    return None

def chatbot_reply(message):
    message = message.strip()
    if not message:
        return "Please type a food name or ask me for a food review."

    food = find_food(message)
    lower = message.lower()

    if food:
        item = FOOD_REVIEWS[food]
        return (
            f"🍽️ {food.title()} Review\n\n"
            f"⭐ Rating: {item['rating']}/5\n"
            f"📝 {item['review']}\n\n"
            f"💡 Tip: {item['tips']}"
        )

    if any(word in lower for word in ["hello", "hi", "hey"]):
        return (
            "Hi! 👋 I’m FoodieBot. Ask me about pizza, burger, biryani, dosa, "
            "noodles, or ice cream."
        )

    if "rating" in lower or "best" in lower or "recommend" in lower:
        return (
            "I can review foods and give ratings. Try: "
            "\"Review biryani\" or \"What is the rating for pizza?\""
        )

    return (
        "I’m a food-review chatbot. 🍴 I currently know about pizza, burger, "
        "biryani, dosa, noodles, and ice cream. Ask me for a review or rating."
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    return jsonify({"reply": chatbot_reply(message)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
