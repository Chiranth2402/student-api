# 🎓 Student Management REST API

## 📌 Description

This project is a backend REST API built using Flask and MySQL.
It supports CRUD operations and includes JWT-based authentication for secure access.

---

## ⚙️ Tech Stack

* Python (Flask)
* MySQL
* Flask-MySQLdb
* JWT Authentication

---

## 🚀 Features

* Add Student (POST)
* Get Students (GET) 🔒 Protected
* Update Student (PUT)
* Delete Student (DELETE)
* User Registration
* User Login
* JWT Token-based Authentication

---

## 🔗 API Endpoints

### 🔐 Authentication

* POST /register
* POST /login

### 📚 Student APIs

* POST /add_student
* GET /students  (Protected)
* PUT /update_student/<id>
* DELETE /delete_student/<id>

---

## 🔑 Authentication Flow

1. Register user
2. Login → Get JWT token
3. Add token in header:
   Authorization: <your_token>
4. Access protected APIs

---

## ▶️ How to Run

1. Clone repository
2. Install dependencies:
   pip install flask flask-mysqldb PyJWT
3. Run:
   python app.py

---

## 📊 Database

* Database: student_db
* Tables:

  * students
  * users

---

## 👨‍💻 Author

Chiranth G H 
