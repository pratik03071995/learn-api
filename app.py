import os
from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = os.getenv('SQLITE_DATABASE_PATH', 'university.db')

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create tables if they don't exist
def create_tables():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# Initialize database when the app starts
@app.before_first_request
def before_first_request():
    create_tables()

# Create a student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if not first_name or not last_name:
        return jsonify({'error': 'Missing required fields'}), 400
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
    db.commit()
    return jsonify({'message': 'Student created successfully'}), 201

# Create a course
@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    name = data.get('name')
    code = data.get('code')
    description = data.get('description')
    if not name or not code or not description:
        return jsonify({'error': 'Missing required fields'}), 400
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO courses (name, code, description) VALUES (?, ?, ?)", (name, code, description))
    db.commit()
    return jsonify({'message': 'Course created successfully'}), 201


# Add enrollment
@app.route('/enrollments', methods=['POST'])
def add_enrollment():
    data = request.get_json()
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    if not student_id or not course_id:
        return jsonify({'error': 'Missing required fields'}), 400
    db = get_db()
    c = db.cursor()
    try:
        c.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
        db.commit()
        return jsonify({'message': 'Enrollment added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Duplicate enrollment'}), 400

# Show all students and which courses the students have taken
@app.route('/students/courses', methods=['GET'])
def get_students_courses():
    db = get_db()
    c = db.cursor()
    query = '''SELECT students.id, students.first_name, students.last_name,
                      courses.id, courses.name, courses.code, courses.description
               FROM students
               LEFT JOIN enrollments ON students.id = enrollments.student_id
               LEFT JOIN courses ON enrollments.course_id = courses.id'''
    c.execute(query)
    students_courses = c.fetchall()
    students = {}
    for row in students_courses:
        student_id, first_name, last_name, course_id, name, code, description = row
        if student_id not in students:
            students[student_id] = {'first_name': first_name, 'last_name': last_name, 'courses': []}
        if course_id:
            students[student_id]['courses'].append({'id': course_id, 'name': name, 'code': code, 'description': description})
    return jsonify(list(students.values()))

# Show all students and which courses the students have not taken
@app.route('/students/not_taken_courses', methods=['GET'])
def get_students_not_taken_courses():
    db = get_db()
    c = db.cursor()
    query = '''SELECT students.id, students.first_name, students.last_name,
                      courses.id, courses.name, courses.code, courses.description
               FROM students
               LEFT JOIN enrollments ON students.id = enrollments.student_id
               LEFT JOIN courses ON enrollments.course_id = courses.id
               WHERE enrollments.student_id IS NULL'''
    c.execute(query)
    students_courses = c.fetchall()
    students = {}
    for row in students_courses:
        student_id, first_name, last_name, course_id, name, code, description = row
        if student_id not in students:
            students[student_id] = {'first_name': first_name, 'last_name': last_name, 'courses': []}
    return jsonify(list(students.values()))

if __name__ == '__main__':
    app.run(debug=True)











