from flask import render_template, request, redirect, url_for
from app import app

# In-memory basket
basket = ["Apple", "Banana", "Orange"]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        fruit = request.form.get("fruit")
        if fruit:
            basket.append(fruit.title())
        return redirect(url_for("home"))
    return render_template("index.html", basket=basket)
