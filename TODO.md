# TODO — finalise l’onboarding zero-touch

## Backend
- [x] Ajouter route `GET /client` pour servir `backend/templates/client.html` (corriger PWA start_url).
- [ ] Ajouter alias `POST /api/update` -> `POST /api/ping` (compatibilité + “puissance” côté client actuel).
- [ ] Vérifier/renforcer `POST /api/zero-touch` : validation `public_key` + création/lookup stable `device_token`.

## Frontend (device client)
- [x] Mettre à jour `backend/templates/client.html` pour utiliser `POST /api/zero-touch`.
- [x] Stocker `device_token` dans `localStorage`.
- [x] Envoyer la télémétrie vers `POST /api/ping` avec header `X-Device-Token`.
- [x] Retirer l’IMEI hardcodé.


## Optionnel
- [x] Mettre à jour `backend/simulateur.py` pour appeler `zero-touch` puis `ping` avec `X-Device-Token`.



## Validation
- [ ] Démarrer le backend et tester :
  - [ ] Ouvrir `/client?public_key=...` (ou `?pk=`) 
  - [ ] Vérifier création Owner+Device et persistance `device_token`
  - [ ] Vérifier que `ping` fonctionne et que les commandes sont délivrées.

