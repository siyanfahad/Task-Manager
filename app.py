from flask import Flask, render_template
from flask import request, jsonify
import sqlite3

app = Flask(__name__)


def init_db():
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT) ')

init_db() 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with sqlite3.connect('tasks.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks')
        tasks = [{'id': row[0], 'title': row[1]} for row in cur.fetchall()]
    return jsonify(tasks)

@app.route('/task', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title', '').strip()

    if not title:
        return jsonify({'error': 'Task title is required'}), 400

    with sqlite3.connect('tasks.db') as conn:
        conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    return jsonify({'message': 'Task added successfully'})

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return jsonify({'message': f'Task {task_id} deleted'})

if __name__ == '__main__':
    app.run(debug=True)

