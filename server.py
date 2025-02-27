from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from datetime import timedelta
import os

# Flask App initialisieren
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'ODyecvPOQrDaEdNhFrR68CB6p8y_kUaPGiyjklWBWY4'  # Starker Schlüssel
app.permanent_session_lifetime = timedelta(minutes=30)  # Sitzungszeit auf 30 Minuten setzen

# Sicherheitsrichtlinien mit Flask-Talisman
Talisman(
    app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
        'style-src': "'self' https://fonts.googleapis.com",
        'font-src': "'self' https://fonts.gstatic.com",
        'img-src': "'self' data:",
    },
    force_https=False,
    strict_transport_security=False
)

# Rate-Limiting
limiter = Limiter(get_remote_address, app=app)

DATABASE = os.path.join(os.path.dirname(__file__), 'wishlist.db')

# Datenbank initialisieren
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Wunschliste-Tabelle
    cursor.execute('''CREATE TABLE IF NOT EXISTS wishlist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        year TEXT NOT NULL,
                        link TEXT,
                        category TEXT NOT NULL,
                        username TEXT NOT NULL)''')
    # Historie-Tabelle
    cursor.execute('''CREATE TABLE IF NOT EXISTS wishlist_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        year TEXT NOT NULL,
                        link TEXT,
                        category TEXT NOT NULL)''')
    # Benutzer-Tabelle
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
    # Admin-Benutzer erstellen, falls nicht vorhanden
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = "admin"')
    if cursor.fetchone()[0] == 0:
        hashed_password = generate_password_hash("adminpassword", method='sha256')
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("admin", hashed_password))
    conn.commit()
    conn.close()

# Datenbank-Verbindung
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    print(f"Using database at: {DATABASE}")
    conn.row_factory = sqlite3.Row  # Rückgabe als Dictionary
    return conn

# Login-Seite
@app.route('/')
def login_page():
    if 'user' in session:  # Benutzer bereits eingeloggt
        return redirect(url_for('serve_index'))
    return render_template('login.html')

# Login-Verarbeitung
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Begrenzung der Login-Versuche
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return render_template('login.html', error="Fehlende Anmeldedaten"), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user'] = username
        session.permanent = True
        return redirect(url_for('serve_index'))
    return render_template('login.html', error="Ungültiger Benutzername oder Passwort"), 401

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

# Index-Seite
@app.route('/index.html')
def serve_index():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

# Wunschliste-Seite
@app.route('/wishlist.html')
def serve_wishlist():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('wishlist.html')

# Eintrag hinzufügen
@app.route('/add_entry', methods=['POST'])
def add_entry():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    if not data or not all(key in data for key in ['title', 'year', 'category']):
        return jsonify({'error': 'Invalid data'}), 400

    username = session['user']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO wishlist (title, year, link, category, username)
                      VALUES (?, ?, ?, ?, ?)''',
                   (data['title'], data['year'], data.get('link', None), data['category'], username))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 201


# Wunschliste abrufen
@app.route('/get_wishlist')
def get_wishlist():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wishlist')
    entries = cursor.fetchall()
    conn.close()

    # Kategorienamen direkt umformatieren
    formatted_entries = []
    for row in entries:
        entry = dict(row)
        category = entry['category']
        if category == "Nicht-Anime":
            entry['category'] = "Film"
        elif category == "Anime":
            entry['category'] = "Anime Film"
        elif category == "Nicht-Anime-Serie":
            entry['category'] = "Serie"
        elif category == "Anime-Serie":
            entry['category'] = "Anime Serie"
        # Weitere Kategorien direkt hier behandeln
        formatted_entries.append(entry)

    return jsonify(formatted_entries)


# Eintrag entfernen
@app.route('/remove_entry/<int:id>', methods=['DELETE'])
def remove_entry(id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Überprüfen, ob der Benutzer Admin ist
    if session['user'] != 'Admin':
        return jsonify({'error': 'Forbidden: Only Admin can remove entries'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM wishlist WHERE id = ?', (id,))
        entry = cursor.fetchone()
        if not entry:
            return jsonify({'error': 'Entry not found'}), 404

        # Verschiebe in die Historie
        cursor.execute('''INSERT INTO wishlist_history (title, year, link, category)
                          SELECT title, year, link, category FROM wishlist WHERE id = ?''', (id,))
        # Lösche den Eintrag
        cursor.execute('DELETE FROM wishlist WHERE id = ?', (id,))
        conn.commit()
        print(f"Entry with ID {id} removed successfully")
    except Exception as e:
        print(f"Error while deleting entry: {e}")
        conn.rollback()
        return jsonify({'error': 'Database error'}), 500
    finally:
        conn.close()

    return '', 204


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=44555, debug=False)  # Debug deaktiviert
