# Task Manager 📋

Une application de gestion de tâches moderne et intuitive, développée en Python avec **PySide6** (Qt6).

## 🎨 Caractéristiques

- ✅ **Interface moderne** avec des formes arrondies et des couleurs vivantes
- ✅ **Gestion complète des tâches** : créer, modifier, supprimer, clôturer
- ✅ **Filtrage par état** : À faire, En cours, Réalisé, Abandonné, En attente
- ✅ **Dates d'échéance et de fin** : suivi complet des délais
- ✅ **Système de commentaires** : ajouter des notes aux tâches
- ✅ **Stockage JSON** : données persistantes
- ✅ **Architecture MVC** : séparation claire entre logique et interface

## 📋 États des tâches

- **À faire** : Tâche non commencée
- **En cours** : Tâche en cours de traitement
- **Réalisé** : Tâche complétée (date de fin enregistrée automatiquement)
- **Abandonné** : Tâche abandonnée
- **En attente** : Tâche en attente

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/SanTaha03/task_manager.git
cd task_manager
```

2. **Créer un environnement virtuel**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Sur macOS/Linux
# ou
.venv\Scripts\activate  # Sur Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python main.py
```

## 📁 Structure du projet

```
task_manager/
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances du projet
├── controllers/
│   └── task_controller.py  # Logique métier
├── models/
│   ├── task.py            # Modèle Task
│   └── enums.py           # Énumérations (TaskState)
├── views/
│   ├── main_window.py     # Fenêtre principale
│   ├── add_task_dialog.py # Dialog d'ajout
│   ├── edit_task_dialog.py# Dialog d'édition
│   └── detail_task_dialog.py# Dialog de détails
├── repositories/
│   └── json_repository.py # Gestion du stockage JSON
├── utils/
│   ├── style_manager.py   # Gestion des styles QSS
│   └── date_format.py     # Formatage des dates
└── data/
    └── tasks.json         # Fichier de données
```

## 🎯 Utilisation

### Ajouter une tâche
1. Cliquez sur le bouton **"Ajouter"** (noir)
2. Remplissez le formulaire (titre obligatoire)
3. Cliquez sur **"Enregistrer"** (vert)

### Modifier une tâche
1. Sélectionnez une tâche dans le tableau
2. Cliquez sur **"Modifier"** (bleu)
3. Modifiez les champs et cliquez sur **"Enregistrer"**

### Clôturer une tâche
1. Sélectionnez une tâche
2. Cliquez sur **"Clôturer la tâche"** (vert)
3. La date de fin sera enregistrée automatiquement

### Supprimer une tâche
1. Sélectionnez une tâche
2. Cliquez sur **"Supprimer"** (rouge)
3. Confirmez la suppression

### Filtrer les tâches
- Utilisez le menu déroulant **"Filtrer par état"** pour afficher uniquement les tâches d'un état spécifique

## 🛠️ Technologies utilisées

- **Python 3.8+**
- **PySide6** : Framework Qt6 pour Python
- **JSON** : Stockage des données

## 👨‍💻 Auteur

Taha Tadil - M2 Développement natif

## 📝 Licence

Ce projet est sous licence MIT.