import requests
import time
import random

URL_API = "http://127.0.0.1:5000/api/update"
IMEI_TEST = "123456789012345"

# Départ
latitude = 6.1375
longitude = 1.2125

print("[XOFIX] Début de la simulation de crise.")
print("Le voleur est en mouvement...")

pas_de_deplacement = 0.0005 # Pas initial (vitesse normale)

for i in range(1, 50):
    # Après 6 requêtes, le voleur monte sur une moto et accélère !
    if i > 6:
        pas_de_deplacement = 0.0018 # On augmente la distance entre les points pour simuler la vitesse
        
    latitude += random.uniform(0, pas_de_deplacement)
    longitude += random.uniform(0, pas_de_deplacement)
    
    data = {
        "imei": IMEI_TEST,
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6)
    }
    
    try:
        res = requests.post(URL_API, json=data)
        if res.status_code == 200:
            mode = "⚡ FUITE RAPIDE" if i > 6 else "🚶 Marche"
            print(f"[Point {i}] Envoyé [{mode}] -> Lat: {data['latitude']} | Lon: {data['longitude']}")
    except:
        print("Erreur serveur")
        
    time.sleep(3)
