from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#   MySQL Database Connection

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@localhost:3308/app_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# PART 1: USER MODEL

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship (User -> Tasks)
    tasks = db.relationship("Task", backref="user", lazy=True)


# PART 3: TASK MODEL (with user_id foreign key)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    # Foreign Key linking task to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# PART 2: USER CRUD ENDPOINTS

# Create user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(
        username=data["username"],
        email=data["email"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


# Get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "created_at": u.created_at
    } for u in users])


# Get single user
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    })


# Update user
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})


# Delete user
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


# PART 3: GET ALL TASKS FOR A USER

@app.route("/api/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    User.query.get_or_404(user_id)  # Check user exists
    tasks = Task.query.filter_by(user_id=user_id).all()

    return jsonify([{
        "id": t.id,
        "title": t.title,
        "completed": t.completed,
        "user_id": t.user_id
    } for t in tasks])

# PART 3: CREATE TASK WITH user_id

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.json

    # Ensure user exists
    User.query.get_or_404(data["user_id"])

    task = Task(
        title=data["title"],
        user_id=data["user_id"]
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created successfully"}), 201


# Run App

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)

