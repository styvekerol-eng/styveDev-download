# ☁️ Guide d'Hébergement Gratuit 24h/24 dans le Cloud

Ce guide vous explique pas à pas comment héberger **StyveDev Download Pro** sur un serveur distant **100% gratuit**, sans que votre PC personnel n'ait besoin de rester allumé.

Tous les fichiers nécessaires (`Dockerfile`, `requirements.txt`, `render.yaml`, `server.py`, `pwa/`) ont déjà été créés et configurés pour vous.

---

## 🏆 Option 1 : Déploiement sur Render.com (Le plus populaire & Recommandé)

Render propose un hébergement gratuit pour les conteneurs Docker avec support complet de **Python**, **FFmpeg** et **WebSockets**.

### Étape 1 : Mettre vos fichiers sur GitHub
1. Si ce n'est pas déjà fait, créez un compte gratuit sur [github.com](https://github.com).
2. Cliquez sur le bouton vert **« New repository »**.
3. Nommez-le par exemple `styvedev-download-pro` et laissez-le en **Public** ou **Private**.
4. Déposez les fichiers suivants dans ce dépôt :
   - `server.py`
   - Le dossier `pwa/` (avec `index.html`, `app.css`, `app.js`, `manifest.json`, `sw.js`, `icons/`)
   - `Dockerfile`
   - `requirements.txt`
   - `render.yaml`
   - `.dockerignore`

### Étape 2 : Lancer le service sur Render
1. Rendez-vous sur [render.com](https://render.com) et cliquez sur **« Sign In »** > **« Continue with GitHub »**.
2. Sur votre tableau de bord Render, cliquez sur le bouton **« New + »** en haut à droite, puis sélectionnez **« Web Service »**.
3. Choisissez l'option **« Build and deploy from a Git repository »**.
4. Sélectionnez votre dépôt `styvedev-download-pro`.
5. Render détecte automatiquement le fichier `Dockerfile` !
6. Choisissez l'offre **« Free »** (0$/mois).
7. Cliquez sur **« Deploy Web Service »**.

### Étape 3 : Votre site est en ligne !
En 2 à 3 minutes, Render construit l'image Docker, installe FFmpeg et démarre votre serveur.
Vous obtenez une adresse permanente en HTTPS du type :
```text
https://styvedev-download-pro.onrender.com
```

👉 Vous pouvez ouvrir cette adresse depuis n'importe quel iPhone, smartphone Android ou ordinateur dans le monde !
Quand un utilisateur télécharge une vidéo, le serveur distant s'occupe de la conversion et le fichier est automatiquement téléchargé dans la galerie/téléchargements du téléphone.

---

## 🥈 Option 2 : Hugging Face Spaces (100% Gratuit à vie, 16 Go RAM)

Hugging Face offre des machines gratuites de 16 Go de RAM avec support Docker sans carte bancaire :

1. Créez un compte sur [huggingface.co](https://huggingface.co).
2. Rendez-vous sur **Spaces** > **« Create new Space »**.
3. Donnez un nom (ex: `styvedev-dl`).
4. Choisissez la licence (ex: `mit`).
5. Sélectionnez le Space SDK : **« Docker »** > **« Blank »**.
6. Cliquez sur **« Create Space »**.
7. Cliquez sur l'onglet **« Files »** > **« Add file »** > **« Upload files »** et déposez :
   - `Dockerfile`
   - `requirements.txt`
   - `server.py`
   - Le dossier `pwa/`
8. Cliquez sur **« Commit changes to main »**.
9. Hugging Face compile et démarre automatiquement le conteneur.
10. Vous obtenez votre URL publique directe :
```text
https://[votre-pseudo]-styvedev-dl.hf.space
```

---

## 💡 Résumé des fichiers prêts dans votre dossier :

| Fichier | Rôle |
|---|---|
| `Dockerfile` | Installe Linux, Python 3.11, FFmpeg et lance le serveur |
| `requirements.txt` | Liste des dépendances Python requises |
| `render.yaml` | Configuration automatique pour Render.com |
| `.dockerignore` | Empêche d'envoyer les fichiers temporaires et les .exe |
| `server.py` | Serveur backend cloud compatible avec les variables d'environnement (`PORT`) |
| `pwa/` | Interface web exacte de `download.py` |
