from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')

DATABASE = 'wishlist.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS wishlist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        year TEXT NOT NULL,
                        link TEXT,
                        category TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS wishlist_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        year TEXT NOT NULL,
                        link TEXT,
                        category TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/wishlist.html')
def serve_wishlist():
    return render_template('wishlist.html')

@app.route('/index.html')
def serve_index_html():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/add_entry', methods=['POST'])
def add_entry():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO wishlist (title, year, link, category)
                      VALUES (?, ?, ?, ?)''',
                   (data['title'], data['year'], data['link'], data['category']))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 201

@app.route('/get_wishlist')
def get_wishlist():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wishlist')
    entries = cursor.fetchall()
    conn.close()
    return jsonify([{'id': row[0], 'title': row[1], 'year': row[2], 'link': row[3], 'category': row[4]} for row in entries])

@app.route('/remove_entry/<int:id>', methods=['DELETE'])
def remove_entry(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO wishlist_history (title, year, link, category)
                      SELECT title, year, link, category FROM wishlist WHERE id = ?''', (id,))
    cursor.execute('DELETE FROM wishlist WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=44555, debug=True)
