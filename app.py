import os
from flask import Flask, render_template, request, redirect, url_for

# Set template folder explicitly
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=template_dir)

# In-memory fruit basket
basket = ["Apple", "Banana", "Orange"]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        fruit = request.form.get("fruit")
        if fruit:
            basket.append(fruit.title())
        return redirect(url_for("home"))
    return render_template("index.html", basket=basket)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
