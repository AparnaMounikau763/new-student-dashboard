from flask import Blueprint, request, jsonify
from .models import Student
from . import db

main = Blueprint('main', __name__)



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



@main.route('/register', methods=['POST'])
def register():
    data = request.json

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return error_response("All fields (username, email, password) are required")

    # Check duplicate username
    if Student.query.filter_by(username=data['username']).first():
        return error_response(
            f"Username '{data['username']}' already exists. Try a different username."
        )

    # Check duplicate email
    if Student.query.filter_by(email=data['email']).first():
        return error_response(
            f"Email '{data['email']}' is already registered. Try logging in."
        )

    student = Student(**data)
    db.session.add(student)
    db.session.commit()

    return success_response("Registered successfully", status_code=201)



@main.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data.get("username") or not data.get("password"):
        return error_response("Username and password are required", 400)

    user = Student.query.filter_by(
        username=data['username'],
        password=data['password']
    ).first()

    if not user:
        return error_response("Invalid username or password", 401)

    return success_response("Login successful", {
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')

    if not query:
        return error_response("Query parameter 'q' is required")

    results = Student.query.filter(Student.username.contains(query)).all()

    data = [
        {
            "id": u.id,
            "username": u.username
        } for u in results
    ]

    return success_response("Search results fetched", data)


@main.route('/students', methods=['GET', 'POST'])
def students():

    if request.method == 'GET':
        students = Student.query.all()

        data = [
            {
                "id": s.id,
                "username": s.username,
                "email": s.email
            } for s in students
        ]

        return success_response("Students fetched", data)

    elif request.method == 'POST':
        data = request.json

        if not data.get("username") or not data.get("email") or not data.get("password"):
            return error_response("All fields (username, email, password) are required")

        # Duplicate checks
        if Student.query.filter_by(username=data['username']).first():
            return error_response(f"Username '{data['username']}' already exists")

        if Student.query.filter_by(email=data['email']).first():
            return error_response(f"Email '{data['email']}' already exists")

        student = Student(**data)
        db.session.add(student)
        db.session.commit()

        return success_response("Student added successfully", status_code=201)

@main.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)

    if not student:
        return error_response("User not found", 404)

    data = {
        "id": student.id,
        "username": student.username,
        "email": student.email
    }

    return success_response("Student fetched", data)


@main.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)

    if not student:
        return error_response("User not found", 404)

    data = request.json

    # Update username
    if data.get('username'):
        existing = Student.query.filter_by(username=data['username']).first()
        if existing and existing.id != id:
            return error_response(f"Username '{data['username']}' already exists")
        student.username = data['username']

    # Update email
    if data.get('email'):
        existing = Student.query.filter_by(email=data['email']).first()
        if existing and existing.id != id:
            return error_response(f"Email '{data['email']}' already exists")
        student.email = data['email']

    db.session.commit()

    updated_data = {
        "id": student.id,
        "username": student.username,
        "email": student.email
    }

    return success_response("Student updated successfully", updated_data)


@main.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)

    if not student:
        return error_response("Student not found", 404)

    db.session.delete(student)
    db.session.commit()

    return success_response("Student deleted successfully")



@main.route('/ready', methods=['GET'])
def ready():
    import time
    import uuid

    start = time.time()

    try:
        unique = str(uuid.uuid4())[:8]
        username = f"health_{unique}"
        email = f"{unique}@mail.com"

        # 1️⃣ Register
        student = Student(username=username, email=email, password="123")
        db.session.add(student)
        db.session.commit()

        # 2️⃣ Login check
        user = Student.query.filter_by(username=username, password="123").first()
        if not user:
            return jsonify({"status": "fail", "step": "login"}), 500

        # 3️⃣ CRUD check
        user.username = f"updated_{unique}"
        db.session.commit()

        fetched = Student.query.get(user.id)
        if not fetched:
            return jsonify({"status": "fail", "step": "crud"}), 500

        # 4️⃣ Search check
        results = Student.query.filter(Student.username.contains("updated")).all()
        if not results:
            return jsonify({"status": "fail", "step": "search"}), 500

        # 5️⃣ Performance check
        end = time.time()
        if (end - start) > 3:
            return jsonify({"status": "fail", "step": "performance"}), 500

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500