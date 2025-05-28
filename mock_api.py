from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True


items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]
next_id = 4


# Моковые пользователи
users = {
    "john": {
        "password": "1234",
        "id": 1,
        "username": "john",
        "name": "John Doe",
        "email": "john@example.com"
    }
}

# Моковая авторизация по токену
def require_auth(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")
        if token != "token-john":
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # для Flask
    return wrapper

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if user and user["password"] == password:
        return jsonify({"token": "token-john"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/profile", methods=["GET"])
@require_auth
def profile():
    user = users["john"]
    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "name": user["name"],
        "email": user["email"]
    })


@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)

@app.route("/items", methods=["POST"])
def add_item():
    global next_id
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400

    new_item = {
        "id": next_id,
        "name": data["name"]
    }
    items.append(new_item)
    next_id += 1
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    for item in items:
        if item["id"] == item_id:
            item["name"] = data.get("name", item["name"])
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"result": "deleted"})


if __name__ == "__main__":
    app.run(port=5000)

