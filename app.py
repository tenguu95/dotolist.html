import os
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'irgendwas_geheimes'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL)')
    conn.commit()
    conn.close()
    init_db ()
@app.route("/")

def home():
    if not session.get('eingeloggt'):
        return redirect(url_for('login'))
        conn = get_db_connection()
        todos = conn.execute('SELECT * FROM todos').fetchall()
        conn.close()
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    aufgabe = request.form.get("aufgabe")
    if aufgabe:
        conn = get_db_connection()
        conn.execute('INSERT INTO todos (task) VALUES (?)', (aufgabe,))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("passwort")
        richtiges_pw = os.getenv("MEIN_APP_PASSWORT", "Lina08122019.")
        
        if pw == richtiges_pw:
            session['eingeloggt'] = True
            return redirect("/")
        else:
            return "Falsches Passwort!"
            
    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear() 
    return redirect("/login")

app.run(debug=True)

