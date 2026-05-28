# TODO — XOFIX Antivol (Refonte sécurité + stabilité)

## Render / Entrypoint (B)
- [x] Vérifier `backend/Procfile` et l’entrypoint gunicorn (app:app vs backend/app.py)
- [x] Mettre à jour `backend/Procfile` si nécessaire

## Backend hardening (A)
- [ ] Centraliser la génération de `correlation_id`
- [ ] Normaliser les validations JSON pour `/api/zero-touch`, `/api/ping`, `/api/event`
- [ ] Ajouter un check explicite de Content-Type: `application/json`
- [ ] Améliorer les performances de `/api/ping` (éviter requêtes superflues)
- [ ] Renforcer contrôle léger des endpoints admin (basé sur les claims JWT, sans ajouter de lourde auth)

## Chiffrement léger (stabilité)
- [ ] Ajouter HMAC optionnel versionné (header `X-Payload-HMAC`) et clé via env `HMAC_KEY`
- [ ] Déchiffrage: non (TLS + HMAC d’intégrité/auth seulement)

## Observabilité
- [ ] Séparer strictement logs d’audit (/backend/logs/) et logs applicatifs
- [ ] Vérifier que le healthcheck reste rapide et stable (`/api/health`)

## Validation
- [ ] Lancer le backend et vérifier:
  - [ ] `GET /api/health`
  - [ ] `POST /api/zero-touch` (création Owner/Device)
  - [ ] `POST /api/ping` avec `X-Device-Token`
- [ ] Contrôler que le front `backend/templates/client.html` reste compatible

