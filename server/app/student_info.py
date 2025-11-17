from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock data
students = {
    '12345': {'name': 'Ayman Haji', 'course': 'Data Science', 'year': 3, 'gpa': 10},
    '67890': {'name': 'Sara Ali', 'course': 'Computer Engineering', 'year': 2, 'gpa': 9.5},
    '11223': {'name': 'John Deo', 'course': 'Information Systems', 'year': 4, 'gpa': 8.8}
}

# Get student info
@app.route('/api/student')
def get_student():
    student_id = request.args.get('id')
    if student_id in students:
        return jsonify(students[student_id])
    else:
        return jsonify({'error': 'Student not found'}), 404

# Get student count
@app.route('/api/students/count')
def student_count():
    count = len(students)
    return jsonify({'total_students': count})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
