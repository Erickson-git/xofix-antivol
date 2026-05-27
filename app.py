import random
import sqlite3
import math
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)
DB_NAME = "antivol.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appareils (
            imei TEXT PRIMARY KEY,
            nom_titulaire TEXT NOT NULL,
            statut TEXT DEFAULT 'actif'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imei TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (imei) REFERENCES appareils(imei)
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM appareils")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO appareils (imei, nom_titulaire, statut) VALUES (?, ?, ?)",
            ("123456789012345", "Appareil Test Komi", "actif")
        )
    conn.commit()
    conn.close()

def calculer_vitesse(lat1, lon1, lat2, lon2, temps_sec):
    """Calcule la vitesse approximative en km/h entre deux coordonnées GPS."""
    if temps_sec <= 0: return 0
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    vitesse_ms = distance / temps_sec
    vitesse_kmh = vitesse_ms * 3.6
    return round(vitesse_kmh, 1)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/client')
def page_client():
    return render_template('client.html')

@app.route('/api/update', methods=['POST'])
def update_location():
    data = request.get_json()
    if not data or 'imei' not in data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({"error": "Donnees invalides"}), 400
        
    imei = data['imei']
    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tracking (imei, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)",
            (imei, latitude, longitude, timestamp)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_tracking_data():
    """Renvoie l'historique recent et calcule la vitesse de fuite instantanee."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT latitude, longitude, timestamp FROM tracking WHERE imei = ? ORDER BY id DESC LIMIT 20",
            ("123456789012345",)
        )
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return jsonify({"error": "Aucune donnee"}), 404
            
        rows.reverse()
        points = [{"latitude": r[0], "longitude": r[1], "timestamp": r[2]} for r in rows]
        
        vitesse = 0
        if len(points) >= 2:
            p_avant_dernier = points[-2]
            p_dernier = points[-1]
            vitesse = calculer_vitesse(
                p_avant_dernier["latitude"], p_avant_dernier["longitude"],
                p_dernier["latitude"], p_dernier["longitude"], 3
            )
            
        return jsonify({
            "vitesse_kmh": vitesse,
            "derniere_position": points[-1],
            "historique_trajet": points
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)