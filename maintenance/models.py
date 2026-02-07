from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
    """Utilisateur personnalisé avec rôles"""
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('TECHNICIEN', 'Technicien'),
        ('EMPLOYE', 'Employé'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYE')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    direction = models.ForeignKey('Direction', on_delete=models.SET_NULL, null=True, blank=True, related_name='employes')
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class Direction(models.Model):
    """Direction de l'entreprise"""
    nom = models.CharField(max_length=200, unique=True)
    
    class Meta:
        verbose_name = 'Direction'
        verbose_name_plural = 'Directions'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Bureau(models.Model):
    """Bureau rattaché à une direction"""
    nom = models.CharField(max_length=200)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='bureaux')
    
    class Meta:
        verbose_name = 'Bureau'
        verbose_name_plural = 'Bureaux'
        ordering = ['direction', 'nom']
        unique_together = ['nom', 'direction']
    
    def __str__(self):
        return f"{self.nom} - {self.direction.nom}"


class CategorieEquipement(models.Model):
    """Catégorie d'équipement (PC, Imprimante, etc.)"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Catégorie d\'équipement'
        verbose_name_plural = 'Catégories d\'équipements'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Equipement(models.Model):
    """Équipement informatique de l'inventaire"""
    code_equipement = models.CharField(max_length=50, unique=True, primary_key=True)
    nom = models.CharField(max_length=200)
    marque = models.CharField(max_length=100)
    date_acquisition = models.DateField()
    description_technique = models.TextField(blank=True, null=True)
    bureau = models.ForeignKey(Bureau, on_delete=models.SET_NULL, null=True, related_name='equipements')
    categorie = models.ForeignKey(CategorieEquipement, on_delete=models.SET_NULL, null=True, related_name='equipements')
    
    class Meta:
        verbose_name = 'Équipement'
        verbose_name_plural = 'Équipements'
        ordering = ['code_equipement']
    
    def __str__(self):
        return f"{self.code_equipement} - {self.nom}"


class DemandeMaintenance(models.Model):
    """Demande de maintenance soumise par un employé"""
    URGENCE_CHOICES = [
        ('BASSE', 'Basse'),
        ('MOYENNE', 'Moyenne'),
        ('HAUTE', 'Haute'),
    ]
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ASSIGNEE', 'Assignée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('VALIDEE', 'Validée'),
        ('REFUSEE', 'Refusée'),
    ]
    
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name='demandes')
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_creees', limit_choices_to={'role': 'EMPLOYE'})
    technicien = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_assignees', limit_choices_to={'role': 'TECHNICIEN'})
    urgence = models.CharField(max_length=20, choices=URGENCE_CHOICES, default='MOYENNE')
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    email_envoye = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Demande de maintenance'
        verbose_name_plural = 'Demandes de maintenance'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Demande #{self.pk} - {self.equipement.code_equipement} ({self.get_statut_display()})"
    
    def peut_etre_modifiee(self):
        """Vérifie si la demande peut être modifiée par l'employé"""
        return self.statut in ['EN_ATTENTE']
    
    def peut_etre_supprimee(self):
        """Vérifie si la demande peut être supprimée par l'employé"""
        return self.statut in ['EN_ATTENTE']
    
    def peut_etre_validee(self):
        """Vérifie si la demande peut être validée/refusée par l'employé"""
        return self.statut == 'TERMINEE'


class Intervention(models.Model):
    """Rapport d'intervention du technicien"""
    TYPE_REPARATION_CHOICES = [
        ('INTERNE', 'Réparation Interne'),
        ('EXTERNE', 'Réparation Externe'),
    ]
    
    demande = models.OneToOneField(DemandeMaintenance, on_delete=models.CASCADE, related_name='intervention')
    details = models.TextField()
    type_reparation = models.CharField(max_length=20, choices=TYPE_REPARATION_CHOICES, default='INTERNE')
    date_intervention = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Intervention'
        verbose_name_plural = 'Interventions'
        ordering = ['-date_intervention']
    
    def __str__(self):
        return f"Intervention #{self.pk} - Demande #{self.demande.pk}"
    
    def cout_total_pieces(self):
        """Calcule le coût total des pièces utilisées"""
        return sum(piece.cout_total() for piece in self.pieces.all())


class PieceRechange(models.Model):
    """Pièce de rechange utilisée lors d'une intervention"""
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='pieces')
    nom = models.CharField(max_length=200)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantite = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    class Meta:
        verbose_name = 'Pièce de rechange'
        verbose_name_plural = 'Pièces de rechange'
    
    def __str__(self):
        return f"{self.nom} (x{self.quantite})"
    
    def cout_total(self):
        """Calcule le coût total (prix unitaire * quantité)"""
        return self.prix_unitaire * self.quantite
    

class FichierIntervention(models.Model):

    TYPE_FICHIER_CHOICES = [
    ('FACTURE', 'Facture'),
    ('PHOTO_AVANT', 'Photo Avant Réparation'),
    ('PHOTO_APRES', 'Photo Après Réparation'),
    ('DEVIS', 'Devis'),
    ('DIAGNOSTIC', 'Rapport de Diagnostic'),
    ('GARANTIE', 'Certificat de Garantie'),
    ('AUTRE', 'Autre Document'),
    ]

    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='fichiers')
    fichier = models.FileField(upload_to='interventions/%Y/%m/', verbose_name='Fichier')
    type_fichier = models.CharField(max_length=20, choices=TYPE_FICHIER_CHOICES, default='AUTRE', verbose_name='Type de fichier')
    description = models.TextField(blank=True, verbose_name='Description')
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ajout')
    ajoute_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ajouté par')
    taille = models.PositiveIntegerField(default=0, verbose_name='Taille (bytes)')

    class Meta:
        verbose_name = 'Fichier d\'intervention'
        verbose_name_plural = 'Fichiers d\'intervention'
        ordering = ['type_fichier', '-date_ajout']

    def __str__(self):
        return f"{self.get_type_fichier_display()} - {self.fichier.name}"

    def save(self, *args, **kwargs):
        """Calcule la taille du fichier avant la sauvegarde"""
        if self.fichier and not self.taille:
            self.taille = self.fichier.size
        super().save(*args, **kwargs)

    def extension(self):
        """Retourne l'extension du fichier"""
        return self.fichier.name.split('.')[-1].lower() if self.fichier else ''

    def est_image(self):
        """Vérifie si le fichier est une image"""
        return self.extension() in ['jpg', 'jpeg', 'png', 'gif', 'bmp']

    def est_pdf(self):
        """Vérifie si le fichier est un PDF"""
        return self.extension() == 'pdf'

    def est_document(self):
        """Vérifie si le fichier est un document Word"""
        return self.extension() in ['doc', 'docx']

    def taille_lisible(self):
        """Retourne la taille en format lisible (KB, MB)"""
        size = self.taille
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    def icone(self):
        """Retourne l'icône Bootstrap appropriée selon le type de fichier"""
        if self.est_image():
            return 'bi-file-image'
        elif self.est_pdf():
            return 'bi-file-pdf'
        elif self.est_document():
            return 'bi-file-word'
        else:
            return 'bi-file-earmark'
    
    

class LogAction(models.Model):
    """Log de traçabilité de toutes les actions dans le système"""
    
    TYPE_ACTION_CHOICES = [
        # Employé
        ('DEMANDE_CREATION', 'Création de demande'),
        ('DEMANDE_MODIFICATION', 'Modification de demande'),
        ('DEMANDE_SUPPRESSION', 'Suppression de demande'),
        ('DEMANDE_VALIDATION', 'Validation de réparation'),
        ('DEMANDE_REFUS', 'Refus de réparation'),
        
        # Technicien
        ('INTERVENTION_CREATION', 'Création de rapport d\'intervention'),
        ('INTERVENTION_MODIFICATION', 'Modification de rapport'),
        ('STATUT_CHANGE', 'Changement de statut'),
        ('FICHIER_UPLOAD', 'Upload de fichier'),
        
        # Admin
        ('ASSIGNATION', 'Assignation de technicien'),
        ('EQUIPEMENT_CREATION', 'Création d\'équipement'),
        ('EQUIPEMENT_MODIFICATION', 'Modification d\'équipement'),
        ('EQUIPEMENT_SUPPRESSION', 'Suppression d\'équipement'),
        ('FICHIER_SUPPRESSION', 'Suppression de fichier'),
        ('IMPORT_CSV', 'Import CSV'),
        ('EXPORT_CSV', 'Export CSV'),
        ('EXPORT_PDF', 'Export PDF'),
        ('EXPORT_WORD', 'Export Word'),
        
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs')
    action = models.CharField(max_length=50, choices=TYPE_ACTION_CHOICES)
    type_objet = models.CharField(max_length=50, blank=True)
    objet_id = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField(blank=True)
    date_action = models.DateTimeField(auto_now_add=True)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Log d\'action'
        verbose_name_plural = 'Logs d\'actions'
        ordering = ['-date_action']
    
    def __str__(self):
        return f"{self.date_action.strftime('%Y-%m-%d %H:%M')} - {self.utilisateur} - {self.get_action_display()}"