# 🌱 Garden Simulator

**Garden Simulator** est un jeu en Python où les joueurs peuvent créer, entretenir et gérer un jardin virtuel. Ils doivent arroser, fertiliser et prendre soin de leurs plantes tout en faisant face à des événements aléatoires qui influencent leur croissance. Le jeu intègre un système économique permettant d’acheter des ressources et de vendre des récoltes.

## 📌 Fonctionnalités principales

### 🌿 Gestion du jardin
- **Planter des graines** : Choisir parmi différentes espèces de plantes (fleurs, légumes, arbres).
- **Arrosage et fertilisation** : Maintenir la santé et accélérer la croissance des plantes.
- **Entretien** : Prendre soin des plantes pour maximiser leur durée de vie.

### 🎲 Événements aléatoires
- **Conditions météorologiques** : Sécheresses et tempêtes affectant la croissance des plantes.
- **Parasites et maladies** : Menaces pouvant réduire la santé des cultures.
- **Événements positifs** : Croissance accélérée en fonction des conditions.

### 💰 Système économique
- **Vente de récoltes** : Les fruits et légumes récoltés sont vendu automatiquement tout les jours (selon une valeur monétaire fixe + un nombre aléatoire de fruit produit).
- **Achat de ressources** : Investir dans de nouvelles parcelles (jusqu’à 15), de l’eau et du fertilisant.

### 💾 Sauvegarde et chargement
- **Partie persistante** : Le joueur peut sauvegarder son jardin et le reprendre plus tard.

## 🏗️ Structure du projet

📂 **GardenSimulator/** *(Racine du dépôt)*
- 📂 **templates** : dossier où sont stockées les fichiers html pour un jeu visuel
- 📂 **templates** : dossier où sont stockées les fichiers css et js pour un jeu visuel et dynamique
- 📄 **main.py** : Fichier principal du jeu (lancement, sauvegarde, gestion générale).
- 📄 **garden.py** : Gestion de la partie dans son état général et des événements aléatoires.
- 📄 **plant.py** : Définition des plantes et de leur cycle de vie.
- 📄 **save.txt** : fichiers contenant la sauvegarde de la partie.
- 📄 **requirements.txt** : Liste des dépendances nécessaires pour exécuter le projet.

## 🚀 Installation et exécution

### 1️⃣ Prérequis
Assurez-vous d’avoir **Python 3.x** installé sur votre machine.

### 2️⃣ Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer le jeu
```bash
python main.py
```

## 📜 Contributeurs
- **Kyrozn** - Créateur et développeur principal.

