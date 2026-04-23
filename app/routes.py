from flask import Blueprint, request, jsonify
from .models import Student
from .extensions import db
import os

main = Blueprint('main', __name__)


# ---------------- RESPONSE HELPERS ---------------- #

def error_response(message, status_code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code


def success_response(message, data=None, status_code=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), status_code


# ---------------- AUTH ---------------- #

@main.route('/register', methods=['POST'])
def register():
    data = request.json

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return error_response("All fields required")

    if Student.query.filter_by(username=data['username']).first():
        return error_response("Username already exists")

    if Student.query.filter_by(email=data['email']).first():
        return error_response("Email already exists")

    student = Student(**data)
    db.session.add(student)
    db.session.commit()

    return success_response("Registered successfully", status_code=201)


@main.route('/login', methods=['POST'])
def login():
    data = request.json

    identifier = data.get("username") or data.get("email")
    password = data.get("password")

    if not identifier or not password:
        return error_response("Username/email and password required", 400)

    user = Student.query.filter(
        (Student.username == identifier) | (Student.email == identifier),
        Student.password == password
    ).first()

    if not user:
        return error_response("Invalid username or password", 401)

    return success_response("Login successful", {
        "id": user.id,
        "username": user.username,
        "email": user.email
    })


# ---------------- SEARCH ---------------- #

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    username = request.args.get('username')

    if query:
        results = Student.query.filter(
            Student.username.like(f"%{query}%")
        ).all()

        data = [{"id": u.id, "username": u.username} for u in results]
        return success_response("Search results fetched", data, 200)

    if username:
        results = Student.query.filter(
            Student.username.contains(username)
        ).all()

        if not results:
            return error_response("No users found", 404)

        data = [{"id": u.id, "username": u.username} for u in results]
        return success_response("Search results fetched", data, 200)

    return error_response("Query required", 400)


# ---------------- STUDENTS CRUD ---------------- #

@main.route('/students', methods=['GET', 'POST'])
def students():

    # 🔥 INTENTIONAL RUNTIME FAILURE ONLY IN DEPLOYMENT
    if os.getenv("BREAK_APP") == "true":
        raise Exception("Intentional crash for rollback testing")

    if request.method == 'POST':
        data = request.get_json()

        if not data or not all(k in data for k in ("username", "email", "password")):
            return error_response("Missing fields")

        if Student.query.filter_by(username=data["username"]).first():
            return error_response("Username already exists")

        if Student.query.filter_by(email=data["email"]).first():
            return error_response("Email already exists")

        student = Student(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )

        db.session.add(student)
        db.session.commit()

        return success_response("Student created", status_code=201)

    students = Student.query.all()
    data = [{
        "id": s.id,
        "username": s.username,
        "email": s.email
    } for s in students]

    return success_response("Students fetched", data)


@main.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return error_response("User not found", 404)

    return success_response("Student fetched", {
        "id": student.id,
        "username": student.username,
        "email": student.email
    })


@main.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return error_response("User not found", 404)

    data = request.json

    if data.get('username'):
        existing_user = Student.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != id:
            return error_response("Username already exists", 400)
        student.username = data['username']

    if data.get('email'):
        existing_email = Student.query.filter_by(email=data['email']).first()
        if existing_email and existing_email.id != id:
            return error_response("Email already exists", 400)
        student.email = data['email']

    db.session.commit()

    return success_response("Student updated successfully")


@main.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return error_response("Student not found", 404)

    db.session.delete(student)
    db.session.commit()

    return success_response("Student deleted successfully")


# ---------------- SYSTEM ---------------- #

@main.route('/system-check', methods=['GET'])
def system_check():
    return jsonify({"status": "ok"}), 200


@main.teardown_app_request
def shutdown_session(exception=None):
    db.session.remove()