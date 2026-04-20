import os
from flask import Flask, render_template, request, redirect, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = "supergeheim"

# Deine Supabase-Verbindung
SUPABASE_URL = "https://tapjtobjoritqqoohrcc.supabase.co"
SUPABASE_KEY = "sb_publishable_TiBy-HS8RieKHfMBVSRi8w_ORIZopwn"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    if not session.get('eingeloggt'):
        return redirect('/login')
    
    # Aufgaben aus Supabase holen
    try:
        response = supabase.table("todos").select("*").execute()
        todos = response.data
    except Exception as e:
        print(f"Fehler: {e}")
        todos = []
        
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    aufgabe = request.form.get("aufgabe")
    if aufgabe:
        # In Supabase speichern
        supabase.table("todos").insert({"task": aufgabe}).execute()
    return redirect("/")

@app.route("/delete/<id>")
def delete(id):
    # Aufgabe löschen
    supabase.table("todos").delete().eq("id", id).execute()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("passwort")
        # Nutzt dein Render-Passwort oder den Standard
        richtiges_pw = os.getenv("MEIN_APP_PASSWORT", "linapipapo")
        if pw == richtiges_pw:
            session['eingeloggt'] = True
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

