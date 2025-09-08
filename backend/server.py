from flask import Flask, request, jsonify, send_from_directory
import json, os, re

app = Flask(__name__, static_folder="../frontend", static_url_path="")

USERS_FILE = "users.json"

# Load users from JSON file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

# Save users to JSON file
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Register endpoint
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users = load_users()

     # Check for empty fields
    if not data.get("firstName", "").strip():
        return jsonify({"error": "First Name is required"}), 400
    if not data.get("lastName", "").strip():
        return jsonify({"error": "Last Name is required"}), 400
    if not data.get("dob", "").strip():
        return jsonify({"error": "Date of Birth is required"}), 400
    if not data.get("username", "").strip():
        return jsonify({"error": "Username is required"}), 400
    if not data.get("password", "").strip():
        return jsonify({"error": "Password is required"}), 400
    if not data.get("confirmPassword", "").strip():
        return jsonify({"error": "Confirm Password is required"}), 400

    # First & Last Name
    if not re.match(r"^[A-Za-z]+$", data.get("firstName", "")):
        return jsonify({"error": "Only letters are allowed in First Name"}), 400
    if not re.match(r"^[A-Za-z]+$", data.get("lastName", "")):
        return jsonify({"error": "Only letters are allowed in Last Name"}), 400

    # Username
    username = data.get("username", "")
    # Case-insensitive uniqueness check
    if any(u["username"].lower() == username.lower() for u in users):
        return jsonify({"error": "Username already taken"}), 400
    # Updated regex for username: 8–25 characters, allowed chars, no email/mobile
    if not re.match(r"^(?!.*@)(?!.*\d{10})[A-Za-z0-9_.-]{8,25}$", username):
        return jsonify({"error": "Invalid username format"}), 400

    # Email
    email = data.get("email", "")
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return jsonify({"error": "Invalid email format"}), 400

    # Mobile (India)
    mobile = data.get("mobile", "")
    if not re.match(r"^[6-9]\d{9}$", mobile):
        return jsonify({"error": "Invalid mobile number"}), 400

    # Password
    password = data.get("password", "")
    confirmPassword = data.get("confirmPassword", "")
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$", password):
        return jsonify({"error": "Password must be 8+ chars with uppercase, lowercase, number, special char"}), 400
    if password != confirmPassword:
        return jsonify({"error": "Passwords do not match"}), 400

    # Save validated user (without storing password for security)
    new_user = {
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "dob": data.get("dob", ""),
        "username": username,
        "email": email,
        "mobile": mobile
    }
    users.append(new_user)
    save_users(users)

    return jsonify({"message": "Registration successful!"})

if __name__ == "__main__":
    app.run(debug=True)
