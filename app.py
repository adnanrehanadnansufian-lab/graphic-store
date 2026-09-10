from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "my_graphic_store_secret_key"

products = [
    {
        "id": 1,
        "name": "Modern Business Poster",
        "price": 15,
        "category": "Posters",
        "image": "design1.jpg",
        "description": "A clean and modern business poster design."
    },
    {
        "id": 2,
        "name": "Instagram Social Media Pack",
        "price": 20,
        "category": "Social Media",
        "image": "design2.jpg",
        "description": "Professional social media templates for Instagram."
    },
    {
        "id": 3,
        "name": "Creative Logo Design",
        "price": 35,
        "category": "Logos",
        "image": "design3.jpg",
        "description": "A professional and creative logo design."
    }
]

@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/shop")
def shop():
    category = request.args.get("category")
    if category:
        filtered_products = [p for p in products if p["category"] == category]
    else:
        filtered_products = products
    return render_template("shop.html", products=filtered_products)

@app.route("/product/<int:product_id>")
def product(product_id):
    selected_product = next((p for p in products if p["id"] == product_id), None)
    if selected_product is None:
        return "Product not found", 404
    return render_template("product.html", product=selected_product)

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])
    if product_id not in cart:
        cart.append(product_id)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    if product_id in cart:
        cart.remove(product_id)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart_ids = session.get("cart", [])
    cart_products = [p for p in products if p["id"] in cart_ids]
    total = sum(p["price"] for p in cart_products)
    return render_template("cart.html", products=cart_products, total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_ids = session.get("cart", [])
    cart_products = [p for p in products if p["id"] in cart_ids]
    total = sum(p["price"] for p in cart_products)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        print("New Order")
        print("Customer:", name)
        print("Email:", email)
        print("Total:", total)

        session["cart"] = []
        return render_template("checkout.html", success=True, total=total)

    return render_template("checkout.html", products=cart_products, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
