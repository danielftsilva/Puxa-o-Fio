from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "puxa-o-fio-2024")

# Secret codes for each checkpoint — change these before deploying
CHECKPOINTS = {
    1: {
        "code": "VARANDA",
        "hint": "Leva o objeto que está na varanda...",
        "location": "Início",
        "description": "Antes de começares, precisas de algo importante.",
        "success_msg": "Levaste o essencial. Agora sim, começa a missão."
    },
    2: {
        "code": "PIRA",
        "hint": "No armário elétrico do 737...",
        "location": "Inicio da missao",
        "description": "Encontra o primeiro código perto do início do caminho.",
        "success_msg": "Checkpoint desbloqueado! Segue o fio..."
    },
    3: {
        "code": "10",
        "hint": "Algumas pessoas chamam-lhe 'arte'; outras, 'vandalismo'...",
        "location": "Ringue de Futebol",
        "description": "Procura o código perto do ringue.",
        "success_msg": "Quase lá..."
    },
    4: {
        "code": "D+C",
        "hint": "Dois corações, uma só árvore...",
        "location": "A Árvore",
        "description": "Encontraste o X. Procura a árvore.",
        "success_msg": "🎉 Missão completa!"
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/checkpoint", methods=["POST"])
def check_code():
    data = request.get_json()
    checkpoint = data.get("checkpoint")
    code = data.get("code", "").strip().upper()

    if checkpoint not in CHECKPOINTS:
        return jsonify({"success": False, "error": "Checkpoint inválido"})

    expected = CHECKPOINTS[checkpoint]["code"].upper()
    if code == expected:
        return jsonify({
            "success": True,
            "message": CHECKPOINTS[checkpoint]["success_msg"],
            "next": checkpoint + 1 if checkpoint < 4 else None
        })
    else:
        return jsonify({"success": False, "error": "Código errado. Tenta outra vez."})

@app.route("/api/checkpoint_info/<int:n>")
def checkpoint_info(n):
    if n not in CHECKPOINTS:
        return jsonify({"error": "Não existe"}), 404
    cp = CHECKPOINTS[n]
    return jsonify({
        "hint": cp["hint"],
        "location": cp["location"],
        "description": cp["description"]
    })

if __name__ == "__main__":
    app.run(debug=True)
