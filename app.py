from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load JSON data securely (update the path to where the file is stored on Render)
# JSON_FILE_PATH = os.getenv("JSON_FILE_PATH", "users.json")

# Helper function to load user data
def load_user_data():
    with open("users.json", "r") as f:
        return json.load(f)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    # Get form data
    username = request.form.get('username')
    password = request.form.get('password')

    # Load user data
    user_data = load_user_data()

    # Authenticate user
    if username in user_data and user_data[username]['password'] == password:
        dashboard_data = user_data[username]['dashboard_data']
        return render_template('dashboard.html', dashboard_data=dashboard_data)

    # Invalid credentials
    return render_template('login.html', error="Invalid username or password")

if __name__ == '__main__':
    app.run(debug=True)
