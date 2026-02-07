from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (User, Direction, Bureau, CategorieEquipement, Equipement,
                     DemandeMaintenance, Intervention, PieceRechange, FichierIntervention, LogAction)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administration des utilisateurs"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'direction', 'is_active']
    list_filter = ['role', 'direction', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'telephone', 'direction')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'telephone', 'direction', 'email', 'first_name', 'last_name')
        }),
    )

@admin.register(LogAction)
class LogActionAdmin(admin.ModelAdmin):
    """Administration des logs d'actions"""
    list_display = ['date_action', 'utilisateur', 'action', 'type_objet', 'objet_id', 'adresse_ip']
    list_filter = ['action', 'date_action', 'utilisateur']
    search_fields = ['utilisateur__username', 'details', 'adresse_ip']
    readonly_fields = ['utilisateur', 'action', 'type_objet', 'objet_id', 'details', 'date_action', 'adresse_ip']
    date_hierarchy = 'date_action'
    
    def has_add_permission(self, request):
        return False  # Pas de création manuelle de logs
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Seul superuser peut supprimer
    
@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Administration des directions"""
    list_display = ['nom']
    search_fields = ['nom']


@admin.register(Bureau)
class BureauAdmin(admin.ModelAdmin):
    """Administration des bureaux"""
    list_display = ['nom', 'direction']
    list_filter = ['direction']
    search_fields = ['nom', 'direction__nom']


@admin.register(CategorieEquipement)
class CategorieEquipementAdmin(admin.ModelAdmin):
    """Administration des catégories d'équipement"""
    list_display = ['nom', 'description']
    search_fields = ['nom']


@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    """Administration des équipements"""
    list_display = ['code_equipement', 'nom', 'marque', 'categorie', 'bureau', 'date_acquisition']
    list_filter = ['categorie', 'marque', 'bureau__direction']
    search_fields = ['code_equipement', 'nom', 'marque']
    date_hierarchy = 'date_acquisition'
    
    fieldsets = (
        ('Identification', {
            'fields': ('code_equipement', 'nom', 'marque')
        }),
        ('Classification', {
            'fields': ('categorie', 'bureau')
        }),
        ('Détails', {
            'fields': ('date_acquisition', 'description_technique')
        }),
    )


class PieceRechangeInline(admin.TabularInline):
    """Inline pour les pièces de rechange"""
    model = PieceRechange
    extra = 1
    fields = ['nom', 'prix_unitaire', 'quantite']


class FichierInterventionInline(admin.TabularInline):
    """Inline pour les fichiers d'intervention"""
    model = FichierIntervention
    extra = 0
    fields = ['fichier', 'type_fichier', 'description', 'ajoute_par', 'taille_lisible']
    readonly_fields = ['ajoute_par', 'taille_lisible']
    
    def taille_lisible(self, obj):
        return obj.taille_lisible() if obj.pk else '-'
    taille_lisible.short_description = 'Taille'


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    """Administration des interventions"""
    list_display = ['id', 'demande', 'type_reparation', 'date_intervention', 'cout_total_pieces', 'nb_fichiers']
    list_filter = ['type_reparation', 'date_intervention']
    search_fields = ['demande__id', 'details']
    date_hierarchy = 'date_intervention'
    inlines = [PieceRechangeInline, FichierInterventionInline]
    
    fieldsets = (
        ('Demande', {
            'fields': ('demande',)
        }),
        ('Intervention', {
            'fields': ('details', 'type_reparation')
        }),
    )
    
    def nb_fichiers(self, obj):
        return obj.fichiers.count()
    nb_fichiers.short_description = 'Fichiers'


@admin.register(FichierIntervention)
class FichierInterventionAdmin(admin.ModelAdmin):
    """Administration des fichiers d'intervention"""
    list_display = ['id', 'intervention', 'type_fichier', 'fichier', 'taille_lisible', 'ajoute_par', 'date_ajout']
    list_filter = ['type_fichier', 'date_ajout']
    search_fields = ['intervention__demande__id', 'description']
    readonly_fields = ['taille', 'date_ajout', 'ajoute_par']
    date_hierarchy = 'date_ajout'
    
    fieldsets = (
        ('Fichier', {
            'fields': ('intervention', 'fichier', 'type_fichier')
        }),
        ('Détails', {
            'fields': ('description', 'taille', 'ajoute_par', 'date_ajout')
        }),
    )


@admin.register(DemandeMaintenance)
class DemandeMaintenanceAdmin(admin.ModelAdmin):
    """Administration des demandes de maintenance"""
    list_display = ['id', 'equipement', 'employe', 'technicien', 'urgence', 'statut', 'date_creation']
    list_filter = ['statut', 'urgence', 'date_creation']
    search_fields = ['equipement__code_equipement', 'employe__username', 'technicien__username', 'description']
    date_hierarchy = 'date_creation'
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Équipement et Utilisateurs', {
            'fields': ('equipement', 'employe', 'technicien')
        }),
        ('Détails de la demande', {
            'fields': ('urgence', 'statut', 'description')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
        ('Notification', {
            'fields': ('email_envoye',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('equipement', 'employe', 'technicien')


@admin.register(PieceRechange)
class PieceRechangeAdmin(admin.ModelAdmin):
    """Administration des pièces de rechange"""
    list_display = ['nom', 'intervention', 'prix_unitaire', 'quantite', 'cout_total']
    list_filter = ['intervention__type_reparation']
    search_fields = ['nom', 'intervention__demande__id']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('intervention', 'intervention__demande')


# Configuration du site admin
admin.site.site_header = "EP Mostaganem - Gestion Maintenance"
admin.site.site_title = "Gestion Maintenance"
admin.site.index_title = "Administration"