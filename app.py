from flask import Flask, render_template

app = Flask(__name__)

# Sample product catalog data for BrightMart
products = [
    {
        "id": 1,
        "name": "Wireless Bluetooth Headphones",
        "price": 49.99,
        "description": "Premium noise-cancelling headphones with 30-hour battery life and crystal-clear sound.",
        "category": "Electronics",
        "image": "🎧"
    },
    {
        "id": 2,
        "name": "Organic Green Tea Set",
        "price": 24.99,
        "description": "Hand-picked organic green tea collection with 6 unique flavors from around the world.",
        "category": "Food & Beverage",
        "image": "🍵"
    },
    {
        "id": 3,
        "name": "Smart Fitness Tracker",
        "price": 79.99,
        "description": "Track steps, heart rate, sleep, and 20+ workout modes with a vibrant AMOLED display.",
        "category": "Electronics",
        "image": "⌚"
    },
    {
        "id": 4,
        "name": "Bamboo Desk Organizer",
        "price": 34.99,
        "description": "Eco-friendly bamboo organizer with compartments for pens, phone, and office supplies.",
        "category": "Home & Office",
        "image": "🗂️"
    },
    {
        "id": 5,
        "name": "Stainless Steel Water Bottle",
        "price": 19.99,
        "description": "Double-walled insulated bottle keeps drinks cold for 24h or hot for 12h. BPA-free.",
        "category": "Lifestyle",
        "image": "💧"
    },
    {
        "id": 6,
        "name": "LED Desk Lamp",
        "price": 42.99,
        "description": "Adjustable brightness and color temperature with USB charging port and touch controls.",
        "category": "Home & Office",
        "image": "💡"
    },
]


@app.route("/")
def index():
    return render_template("index.html", products=products)


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
