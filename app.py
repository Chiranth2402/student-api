from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chiranthgh'
app.config['MYSQL_DB'] = 'student_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return "Student API Connected to MySQL 🚀"


# ✅ ADD STUDENT
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


# ✅ GET STUDENTS
@app.route('/students', methods=['GET'])
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

@app.route('/delete_student/<int:id>', methods=['DELETE'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student deleted successfully"})


# ✅ ALWAYS LAST
if __name__ == '__main__':
    app.run(debug=True)
    
