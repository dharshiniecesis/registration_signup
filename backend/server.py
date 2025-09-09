from flask import Flask, request, jsonify, send_from_directory
import os, re
import pandas as pd   # NEW → Using pandas for Excel operations

app = Flask(__name__, static_folder="../frontend", static_url_path="")

USERS_FILE = "users.xlsx"   # CHANGED → Now storing in Excel instead of JSON


# Load users from Excel
def load_users():
    if os.path.exists(USERS_FILE):
        df = pd.read_excel(USERS_FILE)
        return df.to_dict(orient="records")
    return []


# Save users to Excel
def save_users(users):
    df = pd.DataFrame(users)
    df.to_excel(USERS_FILE, index=False)


# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# Serve users.html
@app.route("/users")
def users_page():
    return send_from_directory(app.static_folder, "users.html")   # NEW


# API → fetch all users for table
@app.route("/get_users")
def get_users():
    users = load_users()
    return jsonify(users)   # NEW → return all users as JSON


# Register endpoint
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users = load_users()

    errors = {}  # NEW → Store field-specific errors

    # Check for empty fields
    if not data.get("firstName", "").strip():
        errors["firstName"] = "First Name is required"
    if not data.get("lastName", "").strip():
        errors["lastName"] = "Last Name is required"
    if not data.get("dob", "").strip():
        errors["dob"] = "Date of Birth is required"
    if not data.get("username", "").strip():
        errors["username"] = "Username is required"
    if not data.get("email", "").strip():
        errors["email"] = "Email is required"
    if not data.get("mobile", "").strip():
        errors["mobile"] = "Mobile Number is required"
    if not data.get("password", "").strip():
        errors["password"] = "Password is required"
    if not data.get("confirmPassword", "").strip():
        errors["confirmPassword"] = "Confirm Password is required"

    if errors:
        return jsonify({"errors": errors}), 400  # CHANGED → Return errors by field

    # First & Last Name
    if not re.match(r"^[A-Za-z ]+$", data["firstName"]):
         errors["firstName"] = "Only letters and spaces are allowed"
    if not re.match(r"^[A-Za-z ]+$", data["lastName"]):
         errors["lastName"] = "Only letters and spaces are allowed"


    # Username
    username = data["username"]
    if any(u["username"].lower() == username.lower() for u in users):
        errors["username"] = "Username already taken"
    if not re.match(r"^(?!.*@)(?!.*\d{10})[A-Za-z0-9_.-]{8,25}$", username):
        errors["username"] = "Invalid username format"

    # Email
    email = data["email"]
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        errors["email"] = "Invalid email format"

    # Mobile
    mobile = data["mobile"]
    if not re.match(r"^[6-9]\d{9}$", mobile):
        errors["mobile"] = "Invalid mobile number"

    # Password
    password = data["password"]
    confirmPassword = data["confirmPassword"]
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$", password):
        errors["password"] = "Password must be 8+ chars with uppercase, lowercase, number, special char"
    if password != confirmPassword:
        errors["confirmPassword"] = "Passwords do not match"

    if errors:
        return jsonify({"errors": errors}), 400  # CHANGED

    # Save validated user (without storing password for security)
    new_user = {
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "dob": data["dob"],
        "username": username,
        "email": email,
        "mobile": mobile
    }
    users.append(new_user)
    save_users(users)

    return jsonify({"message": "Registration successful!"})


if __name__ == "__main__":
    app.run(debug=True)
