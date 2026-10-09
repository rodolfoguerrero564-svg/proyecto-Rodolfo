from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Crear base de datos si no existe
def init_db():
    conn = sqlite3.connect('guardias.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS guardias
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT,
                  telefono TEXT,
                  experiencia TEXT,
                  zona TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect('guardias.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guardias ORDER BY id DESC")
    guardias = c.fetchall()
    conn.close()
    return render_template("index.html", guardias=guardias)

@app.route("/registro", methods=["POST"])
def registro():
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono")
    experiencia = request.form.get("experiencia")
    zona = request.form.get("zona")

    conn = sqlite3.connect('guardias.db')
    c = conn.cursor()
    c.execute("INSERT INTO guardias (nombre, telefono, experiencia, zona) VALUES (?,?,?,?)",
              (nombre, telefono, experiencia, zona))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
