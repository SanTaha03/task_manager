# 🗂️ Task Manager — Gestionnaire de Tâches (Projet Python – PySide6)

Une application de gestion de tâches **modulaire, intuitive et persistante**, développée en **Python 3** avec le framework **PySide6 (Qt6)**.
Ce projet illustre la mise en œuvre complète d’un **pattern MVC**, la gestion des données en **JSON**, et la création d’une interface utilisateur interactive.

---

## 🎯 Objectif pédagogique

L’objectif du projet est de réaliser une application de bureau permettant :

* la **création, modification, suppression et clôture** de tâches,
* le **filtrage dynamique par état** (À faire, En cours, Réalisé, Abandonné, En attente),
* la **gestion de dates** (création, échéance, fin),
* l’ajout et la consultation de **commentaires**,
* la **sauvegarde persistante** via un fichier JSON.

---

## ✨ Fonctionnalités principales

| Fonction                    | Description                                                                   |
| --------------------------- | ----------------------------------------------------------------------------- |
| 🆕 **Créer une tâche**      | Ajout via un dialogue dédié (titre, description, échéance optionnelle).       |
| ✏️ **Modifier une tâche**   | Édition complète (titre, description, état, échéance, ajout de commentaires). |
| 🗑️ **Supprimer une tâche** | Suppression avec confirmation.                                                |
| ✅ **Clôturer une tâche**    | Passage automatique à l’état “Réalisé” et enregistrement de la date de fin.   |
| 🔎 **Filtrer par état**     | Affiche uniquement les tâches selon leur statut actuel.                       |
| 💬 **Commentaires**         | Historique chronologique des remarques liées à une tâche.                     |
| 🕓 **Dates formatées**      | Toutes les dates sont affichées au format français : `07/11/2025 à 09h14`.    |
| 🧱 **Architecture MVC**     | Séparation stricte entre les modèles, la logique et les vues.                 |
| 💾 **Persistance JSON**     | Données sauvegardées automatiquement dans `data/tasks.json`.                  |

---

## 🧩 États disponibles

| État              | Signification                           |
| ----------------- | --------------------------------------- |
| 🟢 **À faire**    | Tâche non commencée                     |
| 🟠 **En cours**   | Tâche en cours d’exécution              |
| 🟣 **En attente** | Bloquée ou suspendue                    |
| 🔴 **Abandonné**  | Non poursuivie                          |
| ✅ **Réalisé**     | Terminée (avec date de fin enregistrée) |

---

## 🧠 Justification des choix techniques

| Élément                   | Choix                      | Motivation                                                              |
| ------------------------- | -------------------------- | ----------------------------------------------------------------------- |
| **Framework GUI**         | PySide6 (Qt6)              | Stable, riche en composants, idéal pour les interfaces modernes.        |
| **Pattern**               | MVC                        | Permet une maintenance et une évolutivité facilitées.                   |
| **Persistance**           | JSON                       | Simple à manipuler, transparent et lisible pour un projet de formation. |
| **Format des dates**      | ISO interne + affichage FR | Lisible à l’écran et cohérent pour le stockage.                         |
| **Langue de l’interface** | Français                   | Adaptée au contexte académique et utilisateur final.                    |

---

## ⚙️ Installation

### 🧾 Prérequis

* Python **3.8+**
* pip installé

### 🚀 Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/SanTaha03/task_manager.git
cd task_manager

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# ou
.venv\Scripts\activate      # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l’application
python main.py
```

---

## 📁 Structure du projet

```
task_manager/
├── main.py                         # Point d’entrée principal (instancie MVC)
├── controllers/
│   └── task_controller.py           # Logique métier et gestion du dépôt JSON
├── models/
│   ├── task.py                      # Modèle de données (Task + Comment)
│   └── enums.py                     # États possibles des tâches
├── views/
│   ├── main_window.py               # Fenêtre principale (liste et actions)
│   ├── add_task_dialog.py           # Dialogue d’ajout
│   ├── edit_task_dialog.py          # Dialogue d’édition / ajout de commentaires
│   └── detail_task_dialog.py        # Fiche détaillée (lecture seule)
├── utils/
│   └── date_format.py               # Formatage des dates en français
├── data/
│   └── tasks.json                   # Fichier de données persistantes
└── requirements.txt                 # Liste des dépendances
```

---

## 🎮 Utilisation

### ➕ Ajouter une tâche

1. Cliquer sur **“Ajouter”**
2. Saisir le titre (obligatoire), description et date
3. Valider avec **“Enregistrer”**

### 📝 Modifier une tâche

1. Sélectionner une tâche dans le tableau
2. Cliquer sur **“Modifier”**
3. Modifier les champs, changer l’état ou ajouter un commentaire
4. Enregistrer

### 👁️ Voir les détails

* Double-cliquer sur une tâche pour ouvrir la **fiche de détail**
* Cliquer sur **“Modifier…”** pour passer à l’édition

### ❌ Supprimer une tâche

1. Sélectionner la tâche
2. Cliquer sur **“Supprimer”**
3. Confirmer la suppression

### ✅ Clôturer une tâche

1. Sélectionner la tâche
2. Cliquer sur **“Clôturer la tâche”**
3. L’état devient *Réalisé* et la date de fin est enregistrée

### 🔍 Filtrer par état

* Utiliser le menu déroulant **“Filtrer par état”** pour trier les tâches selon leur statut

---

## 🧰 Technologies utilisées

| Technologie               | Rôle                                    |
| ------------------------- | --------------------------------------- |
| 🐍 **Python 3.8+**        | Langage principal                       |
| 💠 **PySide6 (Qt6)**      | Interface graphique                     |
| 📄 **JSON**               | Persistance locale des données          |
| 🧩 **Dataclasses & Enum** | Structure et typage fort des modèles    |
| 🕓 **datetime**           | Gestion des horodatages et formatage FR |

---

## 👨‍💻 Auteur

**Taha Tadil**

---

## 📝 Licence

Projet sous licence **MIT** – libre de réutilisation et de modification dans un cadre pédagogique.

