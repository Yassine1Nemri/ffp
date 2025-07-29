from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  title TEXT NOT NULL, 
                  description TEXT, 
                  status TEXT DEFAULT 'pending')''')
    conn.commit()
    conn.close()

# Create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
        
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', 
             (title, description))
    conn.commit()
    task_id = c.lastrowid
    conn.close()
    
    return jsonify({
        'id': task_id,
        'title': title,
        'description': description,
        'status': 'pending'
    }), 201

# Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = [{'id': row[0], 'title': row[1], 'description': row[2], 'status': row[3]} 
             for row in c.fetchall()]
    conn.close()
    return jsonify(tasks)

# Update task status
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status is required'}), 400
        
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    affected = c.rowcount
    conn.close()
    
    if affected == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task updated successfully'})

# Delete a task
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    affected = c.rowcount
    conn.close()
    
    if affected == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)