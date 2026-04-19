from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# 🔐 SECRET KEY (for JWT)
app.config['SECRET_KEY'] = 'mysecret123'

# 🛢️ MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chiranthgh'
app.config['MYSQL_DB'] = 'student_db'

mysql = MySQL(app)

# 🔐 JWT Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing"}), 403

        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({"message": "Invalid token"}), 403

        return f(*args, **kwargs)

    return decorated


# 🏠 Home
@app.route('/')
def home():
    return "Student API Connected to MySQL 🚀"


# 🔐 REGISTER USER
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    username = data['username']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User registered successfully"})


# 🔐 LOGIN (JWT TOKEN)
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data['username']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and user[2] == password:
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({"token": token})

    else:
        return jsonify({"message": "Invalid credentials"}), 401


# ➕ ADD STUDENT
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json

    name = data['name']
    email = data['email']
    course = data['course']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
        (name, email, course)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student added successfully"})


# 📥 GET STUDENTS (🔒 Protected)
@app.route('/students', methods=['GET'])
@token_required
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    students = []

    for row in data:
        students.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "course": row[3]
        })

    return jsonify(students)


# ✏️ UPDATE STUDENT
@app.route('/update_student/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json

    name = data['name']
    email = data['email']
    course = data['course']

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE students SET name=%s, email=%s, course=%s WHERE id=%s",
        (name, email, course, id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student updated successfully"})


# ❌ DELETE STUDENT
@app.route('/delete_student/<int:id>', methods=['DELETE'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student deleted successfully"})


# 🚀 RUN APP
if __name__ == '__main__':
    app.run(debug=True)