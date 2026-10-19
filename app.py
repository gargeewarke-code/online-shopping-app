
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 45000},
    {"id": 2, "name": "Headphones", "price": 1500},
    {"id": 3, "name": "Keyboard", "price": 800},
    {"id": 4, "name": "Mouse", "price": 500},
]

cart = []

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Online Shopping Application</title>
</head>
<body>
    <h1>Online Shopping Application</h1>

    <form method="get">
        <input name="search" placeholder="Search products">
        <button type="submit">Search</button>
    </form>

    <h2>Available Products</h2>
    {% for product in products %}
        <p>
            {{ product.name }} - ₹{{ product.price }}
            <a href="{{ url_for('add_to_cart', product_id=product.id) }}">
                Add to Cart
            </a>
        </p>
    {% else %}
        <p>No products available.</p>
    {% endfor %}

    <h2>Shopping Cart</h2>
    {% for item in cart %}
        <p>{{ item.name }} - ₹{{ item.price }}</p>
    {% else %}
        <p>Your cart is empty.</p>
    {% endfor %}

    <p><strong>Total: ₹{{ total }}</strong></p>
    <p><a href="{{ url_for('place_order') }}">Place Order</a></p>
    {% if message %}
        <h3>{{ message }}</h3>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def home():
    search = request.args.get("search", "").strip().lower()
    filtered_products = [
        p for p in products if search in p["name"].lower()
    ]
    total = sum(item["price"] for item in cart)
    return render_template_string(
        PAGE,
        products=filtered_products,
        cart=cart,
        total=total,
        message=""
    )

@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    product = next(
        (p for p in products if p["id"] == product_id), None
    )
    if product:
        cart.append(product)
    return redirect(url_for("home"))

@app.route("/order")
def place_order():
    if cart:
        cart.clear()
        message = "Order placed successfully!"
    else:
        message = "Your cart is empty. Add a product first."

    return render_template_string(
        PAGE,
        products=products,
        cart=cart,
        total=0,
        message=message
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
