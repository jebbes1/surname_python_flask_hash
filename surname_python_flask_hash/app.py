from flask import Flask, request, jsonify, render_template_string
import hashlib

app = Flask(__name__)

hash_storage = {}

html_template = """
<!doctype html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <form method="POST" action="{{ action }}">
        {% for field in fields %}
            <label>{{ field.label }}</label><br>
            <input type="{{ field.type }}" name="{{ field.name }}" required><br><br>
        {% endfor %}
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@app.route('/sethash', methods=['POST'])
def set_hash():
    data = request.json
    key = data.get("key")
    value = data.get("value")

    if not key or not value:
        return jsonify({"error": "Both 'key' and 'value' are required"}), 400

    hashed_value = hashlib.sha256(value.encode()).hexdigest()
    hash_storage[key] = hashed_value

    return jsonify({"message": "Hash set successfully", "hash": hashed_value})

@app.route('/gethash', methods=['GET'])
def get_hash():
    return jsonify(hash_storage)

@app.route('/login', methods=['GET'])
def login():
    fields = [
        {"label": "Username", "type": "text", "name": "username"},
        {"label": "Password", "type": "password", "name": "password"}
    ]
    return render_template_string(html_template, title="Login", fields=fields, action="/login")

@app.route('/register', methods=['GET'])
def register():
    fields = [
        {"label": "Username", "type": "text", "name": "username"},
        {"label": "Email", "type": "email", "name": "email"},
        {"label": "Password", "type": "password", "name": "password"}
    ]
    return render_template_string(html_template, title="Register", fields=fields, action="/register")

if __name__ == '__main__':
    app.run(debug=True)
