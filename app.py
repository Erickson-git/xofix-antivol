from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Données de test pour ton système XOFIX
DATA = {
    "nom": "Komi Erickson",
    "imei": "358942107483921",
    "modele": "Samsung Galaxy S23",
    "vitesse_kmh": 0.0,
    "derniere_position": {
        "latitude": 6.1372,
        "longitude": 1.2126,
        "timestamp": "2026-05-27 21:15:00",
        "battery": 85
    }
}

@app.route('/')
def index():
    # Envoie les variables nom, imei et modele à ton index.html
    return render_template('index.html', nom=DATA["nom"], imei=DATA["imei"], modele=DATA["modele"])

@app.route('/api/history')
def api_history():
    # L'API que ton JavaScript appelle toutes les 4 secondes
    return jsonify(DATA)

@app.route('/api/command', methods=['POST'])
def api_command():
    return jsonify({"status": "success", "message": "Commande reçue"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
