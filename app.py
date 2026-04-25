from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "puxa-o-fio-2024")

# Secret codes for each checkpoint — change these before deploying
CHECKPOINTS = {
    1: {
        "code": "PIRA",  # <- muda este código
        "hint": "No armário elétrico do 737...",
        "location": "Inicio da missao",
        "description": "Encontra o primeiro código perto do início do caminho.",
        "success_msg": "Checkpoint 1 desbloqueado! Segue o fio..."
    },
    2: {
        "code": "10",  # <- muda este código
        "hint": "Algumas pessoas chamam-lhe 'arte'... outras, 'vandalismo'...",
        "location": "Ringue de Futebol",
        "description": "Procura o código perto do ringue. Olha bem à tua volta.",
        "success_msg": "Checkpoint 2 desbloqueado! Quase lá..."
    },
    3: {
        "code": "D+C",  # <- muda este código — ela vai ver o coração na árvore
        "hint": "Dois corações, uma só árvore...",
        "location": "A Arvore",
        "description": "Encontraste o X. Procura a árvore com o coração gravado. O código está lá.",
        "success_msg": "🎉 Missão completa! Agora escava..."
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
            "next": checkpoint + 1 if checkpoint < len(CHECKPOINTS) else None
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
