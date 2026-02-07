import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_project.settings')
django.setup()

from maintenance.models import *
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

# Créer des utilisateurs
admin = User.objects.create_superuser(
    username='admin',
    email='admin@ep-mostaganem.dz',
    password='admin123',
    first_name='Administrateur',
    last_name='Système',
    role='ADMIN'
)

tech1 = User.objects.create_user(
    username='karim',
    email='karim@ep-mostaganem.dz',
    password='tech123',
    first_name='Karim',
    last_name='Benali',
    role='TECHNICIEN',
    telephone='0555123456'
)

tech2 = User.objects.create_user(
    username='fatima',
    email='fatima@ep-mostaganem.dz',
    password='tech123',
    first_name='Fatima',
    last_name='Meziane',
    role='TECHNICIEN',
    telephone='0666789012'
)

emp1 = User.objects.create_user(
    username='ahmed',
    email='ahmed@ep-mostaganem.dz',
    password='emp123',
    first_name='Ahmed',
    last_name='Bouzid',
    role='EMPLOYE',
    telephone='0777345678'
)

emp2 = User.objects.create_user(
    username='sara',
    email='sara@ep-mostaganem.dz',
    password='emp123',
    first_name='Sara',
    last_name='Khelifi',
    role='EMPLOYE',
    telephone='0555987654'
)

print("✓ Utilisateurs créés")

# Créer des directions
dir_admin = Direction.objects.create(nom="Direction Administrative")
dir_tech = Direction.objects.create(nom="Direction Technique")
dir_comm = Direction.objects.create(nom="Direction Commerciale")

print("✓ Directions créées")

# Créer des bureaux
bur_rh = Bureau.objects.create(nom="Bureau RH", direction=dir_admin)
bur_compta = Bureau.objects.create(nom="Bureau Comptabilité", direction=dir_admin)
bur_info = Bureau.objects.create(nom="Bureau Informatique", direction=dir_tech)
bur_maint = Bureau.objects.create(nom="Bureau Maintenance", direction=dir_tech)

print("✓ Bureaux créés")

# Créer des catégories
cat_pc = CategorieEquipement.objects.create(nom="Ordinateur", description="PC de bureau et portables")
cat_imp = CategorieEquipement.objects.create(nom="Imprimante", description="Imprimantes et scanners")
cat_reseau = CategorieEquipement.objects.create(nom="Matériel Réseau", description="Switches, routeurs, etc.")

print("✓ Catégories créées")

# Créer des équipements
equipements = [
    Equipement.objects.create(
        code_equipement="PC-001",
        nom="Dell OptiPlex 7090",
        marque="Dell",
        date_acquisition=date(2023, 1, 15),
        categorie=cat_pc,
        bureau=bur_info,
        description_technique="Intel i7, 16GB RAM, 512GB SSD"
    ),
    Equipement.objects.create(
        code_equipement="PC-002",
        nom="HP EliteDesk 800",
        marque="HP",
        date_acquisition=date(2023, 3, 20),
        categorie=cat_pc,
        bureau=bur_compta,
        description_technique="Intel i5, 8GB RAM, 256GB SSD"
    ),
    Equipement.objects.create(
        code_equipement="IMP-001",
        nom="HP LaserJet Pro",
        marque="HP",
        date_acquisition=date(2022, 6, 10),
        categorie=cat_imp,
        bureau=bur_rh,
        description_technique="Imprimante laser noir et blanc"
    ),
    Equipement.objects.create(
        code_equipement="SW-001",
        nom="Cisco Catalyst 2960",
        marque="Cisco",
        date_acquisition=date(2021, 11, 5),
        categorie=cat_reseau,
        bureau=bur_info,
        description_technique="Switch 24 ports Gigabit"
    ),
]

print("✓ Équipements créés")

# Créer quelques demandes de test
demande1 = DemandeMaintenance.objects.create(
    equipement=equipements[0],
    employe=emp1,
    urgence='HAUTE',
    description="L'ordinateur ne démarre plus. Écran noir au démarrage.",
    statut='EN_ATTENTE'
)

demande2 = DemandeMaintenance.objects.create(
    equipement=equipements[2],
    employe=emp2,
    urgence='MOYENNE',
    description="L'imprimante affiche un message d'erreur 'Bourrage papier' mais rien n'est bloqué.",
    statut='ASSIGNEE',
    technicien=tech1
)

demande3 = DemandeMaintenance.objects.create(
    equipement=equipements[1],
    employe=emp1,
    urgence='BASSE',
    description="L'ordinateur est très lent lors du démarrage de Windows.",
    statut='EN_COURS',
    technicien=tech2
)

print("✓ Demandes créées")

print("\n" + "="*50)
print("DONNÉES DE TEST CRÉÉES AVEC SUCCÈS !")
print("="*50)
print("\n📝 IDENTIFIANTS DE CONNEXION :")
print("\nAdmin:")
print("  Username: admin")
print("  Password: admin123")
print("\nTechnicien 1:")
print("  Username: karim")
print("  Password: tech123")
print("\nTechnicien 2:")
print("  Username: fatima")
print("  Password: tech123")
print("\nEmployé 1:")
print("  Username: ahmed")
print("  Password: emp123")
print("\nEmployé 2:")
print("  Username: sara")
print("  Password: emp123")
print("\n" + "="*50)