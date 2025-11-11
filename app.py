from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify ({
    'message': 'Welcome to Task Manager API',
    'status': 'running'
    })

@app.route('/hello')
def hello():
    return jsonify ({
    'message': 'Hello, World!'})

@app.route('/api/info')
def info():
    return jsonify ({
    'app_name': 'Task Manager',
    'version': '1.0',
    'author': 'omsekhar'
    })

@app.route('/api/status')
def status():
    return jsonify ({
    'database': 'connected',
    'server': 'running',
    'uptime': '24 hours'
    })

@app.route('/api/greet')
def greet():
    name = request.args.get('name','Guest')

    return jsonify ({
    'message': f'Hello, {name}!',
    'greeting': 'Welcome to Task Manager'
    })
@app.route('/api/add')
def add():
    # Get 'a' and 'b' from query parameters
    a = request.args.get('a', 1)
    b = request.args.get('b', 1)

    # Convert them to integers
    a = int(a)
    b = int(b)

    # Add them together
    c = a + b

    # Return the result as JSON
    return jsonify({
        'result': c,
        'operation': 'addition'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)