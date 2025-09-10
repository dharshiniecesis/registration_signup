from flask import Flask, request, jsonify, send_from_directory
from flask_migrate import Migrate
import re
from models import db, User   # Import db and User model

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# ✅ Configure MySQL Database
# Replace with your MySQL credentials
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/register_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Init DB + Migration
db.init_app(app)
migrate = Migrate(app, db)

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Serve users.html
@app.route("/users")
def users_page():
    return send_from_directory(app.static_folder, "users.html")

# Fetch users from DB
@app.route("/get_users")
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# Register endpoint
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    errors = {}

    # Required fields
    required_fields = ["firstName", "lastName", "dob", "username", "email", "mobile", "password", "confirmPassword"]
    for field in required_fields:
        if not data.get(field, "").strip():
            errors[field] = f"{field.replace('confirmPassword','Confirm Password').capitalize()} is required"

    # Name validation
    if not re.match(r"^[A-Za-z ]+$", data.get("firstName", "")):
        errors["firstName"] = "Only letters and spaces allowed"
    if not re.match(r"^[A-Za-z ]+$", data.get("lastName", "")):
        errors["lastName"] = "Only letters and spaces allowed"

    # Username validation
    if User.query.filter_by(username=data["username"]).first():
        errors["username"] = "Username already taken"
    if not re.match(r"^(?!.*@)(?!.*\d{10})[A-Za-z0-9_.-]{8,25}$", data["username"]):
        errors["username"] = "Invalid username format"

    # Email validation
    if User.query.filter_by(email=data["email"]).first():
        errors["email"] = "Email already registered"
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", data["email"]):
        errors["email"] = "Invalid email format"

    # Mobile validation
    if User.query.filter_by(mobile=data["mobile"]).first():
        errors["mobile"] = "Mobile number already registered"
    if not re.match(r"^[6-9]\d{9}$", data["mobile"]):
        errors["mobile"] = "Invalid mobile number"

    # Password validation
    password = data["password"]
    confirmPassword = data["confirmPassword"]
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$", password):
        errors["password"] = "Password must have 8+ chars, uppercase, lowercase, number, special char"
    if password != confirmPassword:
        errors["confirmPassword"] = "Passwords do not match"

    if errors:
        return jsonify({"errors": errors}), 400

    # Save to DB
    new_user = User(
        firstName=data["firstName"],
        lastName=data["lastName"],
        dob=data["dob"],
        username=data["username"],
        email=data["email"],
        mobile=data["mobile"]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful!"})

if __name__ == "__main__":
    app.run(debug=True)
