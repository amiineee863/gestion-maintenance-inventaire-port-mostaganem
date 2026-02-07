from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Authentification
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # ============= ESPACE EMPLOYÉ =============
    path('employe/', views.employe_dashboard, name='employe_dashboard'),
    path('employe/demande/creer/', views.employe_creer_demande, name='employe_creer_demande'),
    path('employe/demande/<int:pk>/modifier/', views.employe_modifier_demande, name='employe_modifier_demande'),
    path('employe/demande/<int:pk>/supprimer/', views.employe_supprimer_demande, name='employe_supprimer_demande'),
    path('employe/demande/<int:pk>/valider/', views.employe_valider_demande, name='employe_valider_demande'),
    
    # ============= ESPACE TECHNICIEN =============
    path('technicien/', views.technicien_dashboard, name='technicien_dashboard'),
    path('technicien/demande/<int:pk>/', views.technicien_detail_demande, name='technicien_detail_demande'),
    path('technicien/demande/<int:pk>/statut/', views.technicien_changer_statut, name='technicien_changer_statut'),
    path('technicien/demande/<int:pk>/intervention/creer/', views.technicien_creer_intervention, name='technicien_creer_intervention'),
    path('technicien/demande/<int:pk>/intervention/modifier/', views.technicien_modifier_intervention, name='technicien_modifier_intervention'),
    
    # ============= ESPACE ADMIN =============
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Gestion des demandes
    path('admin-dashboard/demandes/', views.admin_liste_demandes, name='admin_liste_demandes'),
    path('admin-dashboard/demande/<int:pk>/assigner/', views.admin_assigner_technicien, name='admin_assigner_technicien'),
    
    # Gestion des équipements
    path('admin-dashboard/equipements/', views.admin_liste_equipements, name='admin_liste_equipements'),
    path('admin-dashboard/equipement/creer/', views.admin_creer_equipement, name='admin_creer_equipement'),
    path('admin-dashboard/equipement/<str:code>/modifier/', views.admin_modifier_equipement, name='admin_modifier_equipement'),
    path('admin-dashboard/equipement/<str:code>/supprimer/', views.admin_supprimer_equipement, name='admin_supprimer_equipement'),
    path('admin-dashboard/equipements/import/', views.admin_import_equipements_csv, name='admin_import_equipements_csv'),
    
    # Exports
    path('admin-dashboard/export/demandes/csv/', views.export_demandes_csv, name='export_demandes_csv'),
    path('admin-dashboard/export/demandes/pdf/', views.export_demandes_pdf, name='export_demandes_pdf'),
    path('admin-dashboard/export/equipements/csv/', views.export_equipements_csv, name='export_equipements_csv'),

    # Consultation des interventions (Admin)
    path('admin-dashboard/interventions/', views.admin_liste_interventions, name='admin_liste_interventions'),
    path('admin-dashboard/intervention/<int:pk>/', views.admin_detail_intervention, name='admin_detail_intervention'),
    path('admin-dashboard/fichier/<int:pk>/supprimer/', views.admin_supprimer_fichier, name='admin_supprimer_fichier'),

    # Exports Intervention
    path('intervention/<int:pk>/export/pdf/', views.export_intervention_pdf, name='export_intervention_pdf'),
    path('intervention/<int:pk>/export/word/', views.export_intervention_word, name='export_intervention_word'),

    # Consultation des logs (Admin)
    path('admin-dashboard/logs/', views.admin_liste_logs, name='admin_liste_logs'),
    path('admin-dashboard/logs/export/csv/', views.admin_export_logs_csv, name='admin_export_logs_csv'),
    path('admin-dashboard/logs/export/pdf/', views.admin_export_logs_pdf, name='admin_export_logs_pdf'),
]