# 🔧 Système de Gestion de Maintenance Informatique - EP Mostaganem

## 📋 Informations Projet

**Application développée pour :** Entreprise Portuaire de Mostaganem  
**Développeurs :** HADJ ALI Mohamed Elamine, ABBES Abdelkader
**Établissement :** École Nationale Polytechnique d'Oran (ENPO)  
**Année :** 2025-2026  


## 🎯 Présentation

Application web complète de gestion de maintenance informatique permettant :
- La gestion du parc informatique (inventaire)
- Le suivi des demandes de maintenance
- La traçabilité complète des interventions
- La génération de rapports PDF/Word
- L'export des données (CSV/PDF)
- La consultation des logs d'actions

---

## ✨ Fonctionnalités Principales

### 👤 Espace Employé
- ✅ Création de demandes via scan de code-barres
- ✅ Suivi en temps réel de l'état des demandes
- ✅ Modification/suppression (si en attente)
- ✅ Validation ou refus des réparations terminées
- ✅ Notification email automatique
- ✅ Restriction par direction (sécurité)
- ✅ Protection contre demandes multiples sur même équipement

### 👨‍🔧 Espace Technicien
- ✅ Liste des demandes assignées
- ✅ Gestion du workflow (Assignée → En cours → Terminée)
- ✅ Création de rapports d'intervention détaillés
- ✅ Ajout de pièces de rechange avec coûts
- ✅ Upload de documents (factures, photos avant/après, devis, diagnostics)
- ✅ Export des rapports en PDF et Word
- ✅ Gestion des types de réparation (Interne/Externe)

### 👨‍💼 Espace Administrateur
- ✅ Dashboard avec statistiques en temps réel
- ✅ Gestion complète des utilisateurs (CRUD)
- ✅ Gestion de l'inventaire (CRUD + Import CSV)
- ✅ Assignation intelligente des techniciens (charge de travail visible)
- ✅ Consultation des interventions avec documents joints
- ✅ Filtres avancés (statut, urgence, technicien, date, équipement, catégorie)
- ✅ Pagination automatique des listes
- ✅ Export des données (CSV/PDF) avec filtres appliqués
- ✅ Import massif d'équipements via CSV
- ✅ **Traçabilité complète** : Logs de toutes les actions avec IP, utilisateur, date
- ✅ Consultation et export des logs (filtrable)

### 🔒 Sécurité & Traçabilité
- ✅ Authentification par rôles (Admin, Technicien, Employé)
- ✅ Permissions strictes par profil
- ✅ Redirection automatique selon rôle
- ✅ Logs de toutes les actions (Création, Modification, Suppression, Connexion)
- ✅ Enregistrement des adresses IP
- ✅ Validation des fichiers uploadés (type + taille max 5MB)
- ✅ Protection CSRF et SQL injection (Django intégré)

---

## 🏗️ Architecture Technique

### Stack Technologique
- **Backend :** Django 5.0 (Python 3.10+)
- **Base de données :** SQLite (dev) / PostgreSQL (production recommandée)
- **Frontend :** Bootstrap 5 + Bootstrap Icons
- **Export PDF :** ReportLab
- **Export Word :** python-docx
- **Stockage fichiers :** Système de fichiers local (media/)

### Modèle de Données

```
User (Custom)
├── Direction (FK) - Rattachement employé
└── Logs (relation reverse)

Direction
├── Bureaux
└── Employés

Bureau
├── Direction (FK)
└── Équipements

Equipement
├── Bureau (FK)
├── Catégorie (FK)
└── Demandes

DemandeMaintenance
├── Equipement (FK)
├── Employé (FK)
├── Technicien (FK, nullable)
├── Statuts : EN_ATTENTE → ASSIGNEE → EN_COURS → TERMINEE → VALIDEE/REFUSEE
└── Intervention (OneToOne)

Intervention
├── DemandeMaintenance (OneToOne)
├── PièceRechange (ForeignKey multiple)
└── FichierIntervention (ForeignKey multiple)

FichierIntervention
├── Intervention (FK)
├── Types : FACTURE, PHOTO_AVANT, PHOTO_APRES, DEVIS, DIAGNOSTIC, GARANTIE
└── Métadonnées complètes

LogAction (Traçabilité)
├── Utilisateur (FK)
├── Action (CHOICE : 20+ types d'actions)
├── Objet concerné (type + ID)
├── Détails textuels
├── Date & Heure
└── Adresse IP
```

---

## 🚀 Installation & Déploiement

### 1️⃣ Prérequis Serveur

**Configuration minimale recommandée :**
- OS : Ubuntu 20.04 LTS / Debian 11+ / CentOS 8+
- CPU : 2 cores
- RAM : 4 GB
- Disque : 20 GB
- Python : 3.10 ou supérieur
- Accès Internet (pour installation initiale)

**Installation des dépendances système :**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# CentOS/RHEL
sudo yum install python3 python3-pip nginx postgresql-server postgresql-contrib -y
```

---

### 2️⃣ Configuration de la Base de Données (Production)

**Option A : PostgreSQL (RECOMMANDÉ pour production)**

```bash
# Démarrer PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Créer la base de données
sudo -u postgres psql

CREATE DATABASE maintenance_db;
CREATE USER maintenance_user WITH PASSWORD 'VotreMotDePasseSecurise';
ALTER ROLE maintenance_user SET client_encoding TO 'utf8';
ALTER ROLE maintenance_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE maintenance_user SET timezone TO 'Africa/Algiers';
GRANT ALL PRIVILEGES ON DATABASE maintenance_db TO maintenance_user;
\q
```

**Option B : SQLite (développement/test uniquement)**
- Pas de configuration nécessaire, fichier db.sqlite3 créé automatiquement

---

### 3️⃣ Installation de l'Application

```bash
# 1. Créer un utilisateur système dédié
sudo useradd -m -s /bin/bash maintenance
sudo su - maintenance

# 2. Télécharger/copier le code source
cd /home/maintenance
# [Transférer votre code ici via git, scp, ou autre]

# 3. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 4. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 5. Installer Gunicorn (serveur WSGI pour production)
pip install gunicorn psycopg2-binary
```

---

### 4️⃣ Configuration de l'Application

**Fichier `maintenance_project/settings.py` - MODIFICATIONS OBLIGATOIRES :**

```python
# 1. SECRET_KEY - CHANGER IMMÉDIATEMENT
SECRET_KEY = 'GÉNÉRER_UNE_NOUVELLE_CLÉ_ALÉATOIRE_LONGUE_ET_COMPLEXE'
# Générer avec : python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. DEBUG - DÉSACTIVER EN PRODUCTION
DEBUG = False  # ❗ IMPORTANT

# 3. ALLOWED_HOSTS - Ajouter votre IP/domaine
ALLOWED_HOSTS = ['192.168.1.100', 'maintenance.ep-mostaganem.dz', 'localhost']

# 4. DATABASE - Configuration PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'maintenance_db',
        'USER': 'maintenance_user',
        'PASSWORD': 'VotreMotDePasseSecurise',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 5. EMAIL - Configuration SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # ou smtp de votre entreprise
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'notifications@ep-mostaganem.dz'
EMAIL_HOST_PASSWORD = 'votre_mot_de_passe_application'
DEFAULT_FROM_EMAIL = 'EP Mostaganem <noreply@ep-mostaganem.dz>'

# 6. SÉCURITÉ - Activer en production
SECURE_SSL_REDIRECT = True  # Si HTTPS configuré
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# 7. STATIC & MEDIA - Chemins de production
STATIC_ROOT = '/home/maintenance/staticfiles'
MEDIA_ROOT = '/home/maintenance/media'
```

---

### 5️⃣ Initialisation de l'Application

```bash
# En tant qu'utilisateur maintenance
cd /home/maintenance/maintenance_ep_mostaganem
source venv/bin/activate

# 1. Créer les tables de la base de données
python manage.py makemigrations
python manage.py migrate

# 2. Créer le super-utilisateur (Admin)
python manage.py createsuperuser
# Username: admin
# Email: admin@ep-mostaganem.dz
# Password: [Choisir un mot de passe fort]

# 3. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 4. Créer les dossiers média
mkdir -p media/interventions

# 5. Définir les permissions
chmod -R 755 media/
chmod -R 755 staticfiles/

# 6. [OPTIONNEL] Charger les données de test
python create_test_data.py
```

---

### 6️⃣ Configuration Gunicorn (Serveur WSGI)

**Créer `/etc/systemd/system/maintenance.service` :**

```ini
[Unit]
Description=Gunicorn daemon for Maintenance EP Mostaganem
After=network.target

[Service]
User=maintenance
Group=www-data
WorkingDirectory=/home/maintenance/maintenance_ep_mostaganem
Environment="PATH=/home/maintenance/venv/bin"
ExecStart=/home/maintenance/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/maintenance/maintenance.sock \
    maintenance_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Démarrer le service :**

```bash
sudo systemctl start maintenance
sudo systemctl enable maintenance
sudo systemctl status maintenance
```

---

### 7️⃣ Configuration Nginx (Reverse Proxy)

**Créer `/etc/nginx/sites-available/maintenance` :**

```nginx
server {
    listen 80;
    server_name 192.168.1.100 maintenance.ep-mostaganem.local;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/maintenance/staticfiles/;
    }

    location /media/ {
        alias /home/maintenance/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/maintenance/maintenance.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

**Activer le site :**

```bash
sudo ln -s /etc/nginx/sites-available/maintenance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### 8️⃣ Configuration HTTPS (Optionnel mais recommandé)

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir le certificat SSL
sudo certbot --nginx -d maintenance.ep-mostaganem.dz

# Le renouvellement est automatique
```

---

## 📊 Utilisation de l'Application

### Premier Démarrage

1. **Accéder à l'interface :** `http://[IP_SERVEUR]` ou `http://maintenance.ep-mostaganem.local`

2. **Connexion Admin :** 
   - Username : `admin`
   - Password : [celui défini lors du createsuperuser]

3. **Configuration Initiale (dans l'ordre) :**
   ```
   1. Créer les Directions (Admin Django ou interface)
   2. Créer les Bureaux rattachés aux Directions
   3. Créer les Catégories d'équipements
   4. Importer ou créer les Équipements
   5. Créer les Utilisateurs (Admin, Techniciens, Employés)
      ⚠️ IMPORTANT : Assigner une Direction à chaque Employé
   ```

4. **Import CSV Équipements :**
   - Télécharger le fichier exemple : `/static/exemple_equipements.csv`
   - Remplir avec vos données
   - Importer via : Admin Dashboard → Gérer l'inventaire → Importer CSV

### Workflow Standard

```
1. EMPLOYÉ crée une demande (scan code-barres)
   ↓ Statut: EN_ATTENTE
   
2. ADMIN assigne un technicien
   ↓ Statut: ASSIGNEE
   
3. TECHNICIEN commence l'intervention
   ↓ Statut: EN_COURS
   
4. TECHNICIEN crée le rapport + upload documents
   ↓ Statut: TERMINEE
   ↓ Email envoyé automatiquement à l'employé
   
5. EMPLOYÉ valide ou refuse la réparation
   ↓ Statut: VALIDEE ou REFUSEE
```

---

## 🔐 Comptes par Défaut (Données de Test)

**⚠️ À SUPPRIMER en production après configuration initiale !**

| Rôle | Username | Password | Email |
|------|----------|----------|-------|
| Admin | admin | admin123 | admin@ep-mostaganem.dz |
| Technicien | karim | tech123 | karim@ep-mostaganem.dz |
| Technicien | fatima | tech123 | fatima@ep-mostaganem.dz |
| Employé | ahmed | emp123 | ahmed@ep-mostaganem.dz |
| Employé | sara | emp123 | sara@ep-mostaganem.dz |

---

## 🛠️ Maintenance & Administration

### Sauvegardes Automatiques

**Script de sauvegarde PostgreSQL - `/home/maintenance/backup.sh` :**

```bash
#!/bin/bash
BACKUP_DIR="/home/maintenance/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Créer le dossier de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarde de la base de données
pg_dump -U maintenance_user maintenance_db > $BACKUP_DIR/db_$DATE.sql

# Sauvegarde des fichiers média
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/maintenance/media/

# Nettoyer les anciennes sauvegardes (garder 30 jours)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Sauvegarde terminée : $DATE"
```

**Automatiser avec cron (sauvegarde quotidienne à 2h du matin) :**

```bash
chmod +x /home/maintenance/backup.sh
crontab -e
# Ajouter :
0 2 * * * /home/maintenance/backup.sh >> /home/maintenance/backup.log 2>&1
```

### Logs de l'Application

```bash
# Logs Gunicorn
sudo journalctl -u maintenance -f

# Logs Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Logs Django (si configurés)
tail -f /home/maintenance/logs/django.log
```

### Commandes Utiles

```bash
# Redémarrer l'application
sudo systemctl restart maintenance

# Mettre à jour l'application
cd /home/maintenance/maintenance_ep_mostaganem
source venv/bin/activate
git pull  # Si utilisation de Git
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart maintenance

# Vider le cache
python manage.py clearsessions

# Créer un nouvel utilisateur admin
python manage.py createsuperuser

# Vérifier l'état du service
sudo systemctl status maintenance
sudo systemctl status nginx
sudo systemctl status postgresql
```

---

## 📈 Monitoring & Performance

### Recommandations Production

1. **Monitoring :**
   - Installer Prometheus + Grafana pour métriques
   - Configurer des alertes (emails/SMS) pour pannes
   - Surveiller l'espace disque (logs + média)

2. **Performance :**
   - Activer le cache Redis pour sessions
   - Optimiser les requêtes avec `select_related()` et `prefetch_related()`
   - Configurer Nginx pour compression gzip
   - Utiliser un CDN pour fichiers statiques (optionnel)

3. **Sécurité :**
   - Firewall : Autoriser uniquement ports 80, 443, 22 (SSH)
   - Fail2ban pour protection anti-bruteforce
   - Mises à jour régulières du système et de Python
   - Rotation des logs avec logrotate

---

## 🐛 Dépannage

### Problème : L'application ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u maintenance -n 50

# Vérifier les permissions
ls -la /home/maintenance/maintenance.sock

# Tester Gunicorn manuellement
cd /home/maintenance/maintenance_ep_mostaganem
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 maintenance_project.wsgi:application
```

### Problème : Erreur 502 Bad Gateway

```bash
# Vérifier que Gunicorn fonctionne
sudo systemctl status maintenance

# Vérifier la config Nginx
sudo nginx -t

# Redémarrer les services
sudo systemctl restart maintenance
sudo systemctl restart nginx
```

### Problème : Fichiers statiques non chargés

```bash
cd /home/maintenance/maintenance_ep_mostaganem
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Problème : Erreur de base de données

```bash
# Vérifier PostgreSQL
sudo systemctl status postgresql

# Se connecter à la DB
sudo -u postgres psql maintenance_db

# Vérifier les connexions
\dt  # Lister les tables
\q   # Quitter
```

---

## 📞 Support & Maintenance

### Contact Développeur

Pour toute assistance, bug, ou demande d'évolution :

- **Développeur :** HADJ ALI Mohamed Elamine
- **Email :** hadjali.mohamed.elamine@gmail.com
- **Téléphone :** +213 656 410 106

### Services Proposés

- ✅ Support technique et dépannage
- ✅ Formation des utilisateurs
- ✅ Ajout de nouvelles fonctionnalités
- ✅ Migration de données
- ✅ Optimisation des performances
- ✅ Adaptation aux besoins spécifiques

### Contrat de Maintenance (Optionnel)

Possibilité de souscrire à un contrat de maintenance incluant :
- Support prioritaire 24/7
- Mises à jour de sécurité
- Sauvegardes externalisées
- Monitoring proactif
- Interventions sur site si nécessaire

---

## 📄 Licence & Propriété Intellectuelle

**Propriété :** Entreprise Portuaire de Mostaganem  
**Développement :** HADJ Mohamed Elamine (ENPO)  
**Année :** 2025-2026  

© Tous droits réservés. Cette application est la propriété exclusive de l'Entreprise Portuaire de Mostaganem.

---

## 🙏 Remerciements

Merci à :
- L'équipe de l'Entreprise Portuaire de Mostaganem pour leur confiance
- L'École Nationale Polytechnique d'Oran (ENPO)
- La communauté Django pour les outils et la documentation

---

## 📚 Annexes

### Structure des Dossiers

```
maintenance_ep_mostaganem/
├── maintenance/                 # Application Django
│   ├── migrations/             # Migrations de base de données
│   ├── templates/              # Templates HTML
│   │   └── maintenance/
│   │       ├── employe/
│   │       ├── technicien/
│   │       └── admin/
│   ├── models.py               # Modèles de données
│   ├── views.py                # Logique métier
│   ├── forms.py                # Formulaires
│   ├── urls.py                 # Routes
│   └── admin.py                # Configuration admin Django
├── maintenance_project/        # Configuration projet
│   ├── settings.py            # ⚠️ À configurer
│   ├── urls.py
│   └── wsgi.py
├── static/                     # Fichiers statiques (CSS, JS)
│   └── exemple_equipements.csv
├── media/                      # Fichiers uploadés
│   └── interventions/
├── templates/                  # Templates globaux
├── manage.py                   # Script Django
├── requirements.txt            # Dépendances Python
├── create_test_data.py        # Données de test
└── README.md                   # Ce fichier
```

### Technologies & Versions

```
Python: 3.10+
Django: 5.0
Bootstrap: 5.3
PostgreSQL: 13+ (recommandé)
Nginx: 1.18+
Gunicorn: 20+
ReportLab: 4.0+
python-docx: 1.1+
```

---

**📅 Dernière mise à jour :** Février 2026  
**📝 Version du document :** 1.0  
**✍️ Rédigé par :** HADJ Mohamed Elamine

---

## 🚀 Démarrage Rapide (Résumé)

```bash
# 1. Installer les dépendances système
sudo apt install python3 python3-pip python3-venv postgresql nginx -y

# 2. Configurer PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE maintenance_db;"
sudo -u postgres psql -c "CREATE USER maintenance_user WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE maintenance_db TO maintenance_user;"

# 3. Installer l'application
cd /chemin/vers/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configurer settings.py (SECRET_KEY, DEBUG=False, DATABASES, ALLOWED_HOSTS)

# 5. Initialiser
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# 6. Lancer (Dev)
python manage.py runserver 0.0.0.0:8000

# 7. Production : Configurer Gunicorn + Nginx (voir section déploiement)
```

---

** Bonne utilisation et merci pour votre confiance !**
