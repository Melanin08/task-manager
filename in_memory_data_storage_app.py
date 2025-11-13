from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory data storage
tasks = []
categories = []
task_id_counter = 1
category_id_counter = 1



# PART 1: Add Categories to Tasks

# Create a category
@app.route('/api/categories', methods=['POST'])
def create_category():
    global category_id_counter
    data = request.get_json()

    if not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400

    new_category = {
        'id': category_id_counter,
        'name': data['name']
    }

    categories.append(new_category)
    category_id_counter += 1
    return jsonify({'message': 'Category created', 'category': new_category}), 201


# Get all categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': categories, 'count': len(categories)}), 200


# Create a task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    # Validate category if provided
    category_id = data.get('category_id')
    if category_id and not any(c['id'] == category_id for c in categories):
        return jsonify({'error': 'Invalid category ID'}), 400

    # Validate priority
    priority = data.get('priority', 'medium').lower()
    if priority not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Priority must be low, medium, or high'}), 400

    # Validate due date if provided
    due_date = data.get('due_date')
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400

    new_task = {
        'id': task_id_counter,
        'title': title,
        'description': data.get('description', ''),
        'category_id': category_id,
        'due_date': due_date,
        'completed': False,
        'priority': priority
    }

    tasks.append(new_task)
    task_id_counter += 1
    return jsonify({'message': 'Task created', 'task': new_task}), 201


# Get tasks (with optional category filter)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    category_filter = request.args.get('category_id')
    filtered_tasks = tasks

    if category_filter:
        filtered_tasks = [t for t in tasks if str(t.get('category_id')) == category_filter]

    return jsonify({'tasks': filtered_tasks, 'count': len(filtered_tasks)}), 200


# PART 2: Add Due Dates and Overdue

@app.route('/api/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    today = datetime.today().date()
    overdue = []

    for task in tasks:
        if task['due_date'] and not task['completed']:
            try:
                due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                if due_date < today:
                    overdue.append(task)
            except ValueError:
                continue

    return jsonify({'overdue_tasks': overdue, 'count': len(overdue)}), 200



# PART 3: Statistics Endpoint

@app.route('/api/tasks/stats', methods=['GET'])
def task_stats():
    total = len(tasks)
    completed = len([t for t in tasks if t['completed']])
    pending = total - completed

    today = datetime.today().date()
    overdue = 0
    for t in tasks:
        if t['due_date'] and not t['completed']:
            try:
                if datetime.strptime(t['due_date'], "%Y-%m-%d").date() < today:
                    overdue += 1
            except ValueError:
                pass

    return jsonify({
        'total_tasks': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue
    }), 200



# Run the Application

if __name__ == '__main__':
    app.run(debug=True, port=5008)
