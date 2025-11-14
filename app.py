from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# In-memory storage for fruits
fruit_basket = [
    {"id": 1, "name": "Apple", "quantity": 5, "color": "Red"},
    {"id": 2, "name": "Banana", "quantity": 8, "color": "Yellow"},
    {"id": 3, "name": "Orange", "quantity": 3, "color": "Orange"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Fruit Basket App V1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .fruit-item {
            padding: 15px;
            margin: 10px 0;
            background: #f9f9f9;
            border-left: 4px solid #4CAF50;
            border-radius: 5px;
        }
        .add-form {
            margin-top: 30px;
            padding: 20px;
            background: #e8f5e9;
            border-radius: 5px;
        }
        input[type="text"], input[type="number"] {
            padding: 8px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
        .delete-btn {
            background: #f44336;
            margin-left: 10px;
        }
        .delete-btn:hover {
            background: #da190b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍎 Fruit Basket App v1 🍌</h1>
        <h3>Current Fruits:</h3>
        {% if fruits %}
            {% for fruit in fruits %}
            <div class="fruit-item">
                <strong>{{ fruit.name }}</strong> - 
                Color: {{ fruit.color }} | 
                Quantity: {{ fruit.quantity }}
                <button class="delete-btn" onclick="deleteFruit({{ fruit.id }})">Delete</button>
            </div>
            {% endfor %}
        {% else %}
            <p>No fruits in the basket yet!</p>
        {% endif %}
        
        <div class="add-form">
            <h3>Add New Fruit:</h3>
            <form onsubmit="addFruit(event)">
                <input type="text" id="name" placeholder="Fruit Name" required>
                <input type="text" id="color" placeholder="Color" required>
                <input type="number" id="quantity" placeholder="Quantity" min="1" required>
                <button type="submit">Add Fruit</button>
            </form>
        </div>
    </div>

    <script>
        function addFruit(e) {
            e.preventDefault();
            const data = {
                name: document.getElementById('name').value,
                color: document.getElementById('color').value,
                quantity: parseInt(document.getElementById('quantity').value)
            };
            
            fetch('/api/fruits', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(() => location.reload());
        }
        
        function deleteFruit(id) {
            fetch('/api/fruits/' + id, {method: 'DELETE'})
            .then(() => location.reload());
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, fruits=fruit_basket)

@app.route('/api/fruits', methods=['GET', 'POST'])
def fruits():
    if request.method == 'GET':
        return jsonify(fruit_basket)
    
    if request.method == 'POST':
        data = request.get_json()
        new_id = max([f['id'] for f in fruit_basket], default=0) + 1
        new_fruit = {
            'id': new_id,
            'name': data['name'],
            'color': data['color'],
            'quantity': data['quantity']
        }
        fruit_basket.append(new_fruit)
        return jsonify(new_fruit), 201

@app.route('/api/fruits/<int:fruit_id>', methods=['DELETE'])
def delete_fruit(fruit_id):
    global fruit_basket
    fruit_basket = [f for f in fruit_basket if f['id'] != fruit_id]
    return '', 204

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
