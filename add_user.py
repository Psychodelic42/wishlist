import random
import string
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def generate_password(length=12):
    """
    Generiert ein sicheres Passwort mit einer Mischung aus Großbuchstaben, Kleinbuchstaben,
    Zahlen und Sonderzeichen.

    :param length: Länge des Passworts (Standard: 12)
    :return: Ein zufälliges Passwort als String
    """
    if length < 8:
        raise ValueError("Passwörter sollten mindestens 8 Zeichen lang sein.")

    # Zeichengruppen
    lower = string.ascii_lowercase  # Kleinbuchstaben
    upper = string.ascii_uppercase  # Großbuchstaben
    digits = string.digits          # Zahlen
    special = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"  # Sonderzeichen

    # Mindestens einen Charakter aus jeder Gruppe
    all_chars = lower + upper + digits + special
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(special)
    ]

    # Restliche Zeichen zufällig auffüllen
    password += random.choices(all_chars, k=length - 4)

    # Passwort zufällig mischen
    random.shuffle(password)

    return ''.join(password)

# Beispielaufruf
print(generate_password(16))  # Erzeugt ein Passwort mit 16 Zeichen

DATABASE = os.path.join(os.path.dirname(__file__), 'wishlist.db')

def generate_pw_hash(password):
    return generate_password_hash(password, method='sha256')

# Datenbank initialisieren
def add_user_to_db(user, pw):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Prüfen, ob Tabelle existiert
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        print("Die Tabelle 'users' existiert nicht.")
        conn.close()
        return

    # Benutzer hinzufügen
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (user,))
    if cursor.fetchone()[0] == 0:
        hashed_password = generate_pw_hash(pw)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user, hashed_password))
    conn.commit()
    conn.close()

def main():
    #User
    user = ["Mo","Hazi","Paul","Admin"]

    # Generate Users in DB
    for i in user:

        a = generate_password()
        add_user_to_db(i, a)
        print(f"User: {i} Password: {a} --- added to database")
    return f"{len(user)} Benutzer angelegt."

a = generate_password()
add_user_to_db("Jo",a)
print(a)