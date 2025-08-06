from flask import Flask, render_template, jsonify, request
import json, os
from threading import Lock

app = Flask(__name__, static_folder="static", template_folder="templates")
lock = Lock()

DATA_FILE = "votos.json"

def cargar_votos():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"condena": 0, "salvacion": 0}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_votos(votos):
    with open(DATA_FILE, "w") as f:
        json.dump(votos, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/votos", methods=["GET"])
def obtener_votos():
    votos = cargar_votos()
    return jsonify(votos)

@app.route("/votar", methods=["POST"])
def votar():
    opcion = request.json.get("opcion")
    if opcion not in ["condena", "salvacion"]:
        return jsonify({"error": "Opción inválida"}), 400
    with lock:
        votos = cargar_votos()
        votos[opcion] += 1
        guardar_votos(votos)
    return jsonify({"mensaje": "Voto registrado con éxito"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
