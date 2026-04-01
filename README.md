# 🎓 PreSkool — Système de Gestion Scolaire

Lien de video : video 

> Application web complète de gestion scolaire développée avec **Django (Python)**  
> Projet de Fin de Module · Développement Web Avancé Back-end · FSTG 2025–2026

---

## 👥 Auteurs

| Nom | Rôle |
|-----|------|
| Adil El Bahlouli | Développeur Full-Stack |
| Oussama El Boualiti | Développeur Full-Stack |

**Encadrante :** Mme. Sara Ahsain

---

## 📋 Description

PreSkool est une plateforme web centralisée qui digitalise l'ensemble des opérations académiques et administratives d'un établissement scolaire. Elle remplace les processus manuels (fichiers Excel, plannings papier) par des interfaces intuitives adaptées à chaque rôle.

**Trois types d'utilisateurs :**
- 🔴 **Administrateur** — accès complet à tous les modules
- 🟡 **Enseignant** — gestion pédagogique (examens, notes, emploi du temps)
- 🟢 **Étudiant** — consultation de ses résultats, emploi du temps et examens

---

## ✨ Fonctionnalités

| Module | Fonctionnalités |
|--------|----------------|
| 🔐 Authentification | Connexion multi-rôles, tokens de session, récupération de mot de passe |
| 👨‍🎓 Étudiants | Profils, informations parentales, photos, numéros d'admission, export CSV |
| 👨‍🏫 Enseignants | Profils, qualifications, expérience, affectation aux départements |
| 🏫 Départements | CRUD complet, attribution des chefs de département |
| 📚 Matières | Association matière – département – enseignant |
| 📝 Examens | Planification, créneaux horaires, suivi par classe |
| 📊 Résultats | Saisie des notes, statut automatique (Passé ≥ 10/20), graphiques |
| 🗓️ Emploi du temps | Planification hebdomadaire (lundi–samedi), gestion des salles |
| 🎉 Congés | Calendrier des jours fériés (Public / Scolaire / Autre) |
| 📬 Propositions | Workflow de soumission et approbation de séances supplémentaires |

---

## 🛠️ Stack Technique

**Back-end**
- Python 3.x
- Django 6.0.3
- SQLite3 (développement) → PostgreSQL / MySQL (production)
- Pillow 10.0.0

**Front-end**
- HTML5 / CSS3
- Bootstrap
- JavaScript / jQuery
- DataTables

---

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/Oboualiti/School-PFM-Django-.git 
cd preskool

# 2. Créer et activer un environnement virtuel
python -m venv env
source env/bin/activate        # Linux / macOS
env\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un super-utilisateur
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

L'application est accessible sur **http://127.0.0.1:8000**

---

## 📁 Structure du Projet

```
school/                    ← Projet principal Django
├── home_auth/             ← Authentification & gestion des utilisateurs
│   ├── models.py          ← CustomUser (AbstractUser)
│   ├── views.py           ← Login, logout, register
│   └── urls.py
├── student/               ← Gestion des étudiants
│   ├── models.py          ← Student, Parent
│   ├── views.py           ← CRUD étudiants
│   └── forms.py
├── staff/                 ← Gestion des enseignants
│   ├── models.py          ← Teacher
│   └── views.py
├── academic/              ← Modules académiques
│   ├── models.py          ← Department, Class, Subject, Exam, Grade
│   └── views.py
├── timetable/             ← Emplois du temps & propositions
│   ├── models.py          ← TimeTable, Proposal
│   └── views.py
├── templates/             ← Gabarits HTML
├── static/                ← Fichiers CSS, JS, images
├── media/                 ← Fichiers uploadés (photos étudiants)
└── manage.py
```

---

## ⚙️ Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
SECRET_KEY=secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 📦 requirements.txt

```
Django==6.0.3
Pillow==10.0.0
```

---

## 🔮 Améliorations Prévues

- [ ] Portail parental (suivi des notes et absences)
- [ ] Messagerie interne entre rôles
- [ ] Génération de bulletins de notes en PDF
- [ ] Gestion des absences avec taux de présence
- [ ] API RESTful (Django REST Framework)
- [ ] Déploiement Docker + Docker Compose
- [ ] Authentification 2FA pour les administrateurs
- [ ] Migration vers PostgreSQL en production

---

## 📄 Licence

Ce projet est réalisé dans un cadre académique à la **Faculté des Sciences et Techniques de Tanger (FSTG)**.  
© 2025–2026 Adil El Bahlouli & Oussama El Boualiti
