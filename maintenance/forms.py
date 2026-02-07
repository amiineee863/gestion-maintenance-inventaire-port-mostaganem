from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (User, Direction, Bureau, CategorieEquipement, Equipement,
                     DemandeMaintenance, Intervention, PieceRechange, FichierIntervention, LogAction)
from django.forms import inlineformset_factory


class UserRegistrationForm(UserCreationForm):
    """Formulaire de création d'utilisateur"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }


class UserUpdateForm(forms.ModelForm):
    """Formulaire de modification d'utilisateur"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EquipementForm(forms.ModelForm):
    """Formulaire de création/modification d'équipement"""
    class Meta:
        model = Equipement
        fields = ['code_equipement', 'nom', 'marque', 'date_acquisition', 
                  'description_technique', 'bureau', 'categorie']
        widgets = {
            'code_equipement': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'date_acquisition': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description_technique': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bureau': forms.Select(attrs={'class': 'form-select'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
        }


class DemandeMaintenanceForm(forms.ModelForm):
    """Formulaire de création de demande par l'employé"""
    code_equipement = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Saisissez le code-barres par exemple: PC-001',
            'autofocus': True
        }),
        label='Code-barres de l\'équipement'
    )
    
    class Meta:
        model = DemandeMaintenance
        fields = ['urgence', 'description']
        widgets = {
            'urgence': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 
                                                   'placeholder': 'Décrivez le problème rencontré...'}),
        }
        labels = {
            'urgence': 'Niveau d\'urgence',
            'description': 'Description de la panne',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def clean_code_equipement(self):
        code = self.cleaned_data.get('code_equipement')
        
        # Vérifier si l'équipement existe
        try:
            equipement = Equipement.objects.get(code_equipement=code)
        except Equipement.DoesNotExist:
            raise forms.ValidationError(
                f"Aucun équipement trouvé avec le code '{code}'. Veuillez vérifier le code-barres."
            )
        
        # Vérifier si l'employé est dans la même direction que l'équipement
        if self.user and self.user.direction:
            if equipement.bureau and equipement.bureau.direction != self.user.direction:
                raise forms.ValidationError(
                    f"Équipement hors de votre direction. Cet équipement appartient à la direction '{equipement.bureau.direction.nom}'."
                )
        
        # Vérifier si l'équipement est déjà en maintenance
        demandes_en_cours = DemandeMaintenance.objects.filter(
            equipement=equipement,
            statut__in=['EN_ATTENTE', 'ASSIGNEE', 'EN_COURS', 'TERMINEE']
        ).exclude(pk=self.instance.pk if self.instance else None)

        if demandes_en_cours.exists():
            demande_active = demandes_en_cours.first()
            raise forms.ValidationError(
                f"Cet équipement est déjà en maintenance (Demande #{demande_active.pk} - {demande_active.get_statut_display()}). "
                f"Veuillez attendre la fin de la réparation en cours."
            )

        
        return code
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        code = self.cleaned_data.get('code_equipement')
        instance.equipement = Equipement.objects.get(code_equipement=code)
        if commit:
            instance.save()
        return instance


class AssignationTechnicienForm(forms.ModelForm):
    """Formulaire d'assignation d'un technicien (Admin)"""
    class Meta:
        model = DemandeMaintenance
        fields = ['technicien']
        widgets = {
            'technicien': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.db.models import Q, Count
        
        # Annoter chaque technicien avec le nombre de demandes en cours
        techniciens = User.objects.filter(role='TECHNICIEN', is_active=True).annotate(
            nb_demandes=Count('demandes_assignees', filter=Q(demandes_assignees__statut__in=['ASSIGNEE', 'EN_COURS']))
        ).order_by('nb_demandes', 'first_name')
        
        self.fields['technicien'].queryset = techniciens
        self.fields['technicien'].required = True
        self.fields['technicien'].label_from_instance = lambda obj: f"{obj.get_full_name()} ({obj.nb_demandes} en cours)"


class InterventionForm(forms.ModelForm):
    """Formulaire de création de rapport d'intervention"""
    class Meta:
        model = Intervention
        fields = ['details', 'type_reparation']
        widgets = {
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 
                                              'placeholder': 'Décrivez les actions effectuées...'}),
            'type_reparation': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'details': 'Détails de l\'intervention',
            'type_reparation': 'Type de réparation',
        }


class PieceRechangeForm(forms.ModelForm):
    """Formulaire d'ajout de pièce de rechange"""
    class Meta:
        model = PieceRechange
        fields = ['nom', 'prix_unitaire', 'quantite']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 
                                           'placeholder': 'Ex: Disque dur 1TB'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 
                                                       'step': '0.01', 'min': '0.01'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 
                                                  'min': '1', 'value': '1'}),
        }
        labels = {
            'nom': 'Nom de la pièce',
            'prix_unitaire': 'Prix unitaire (DA)',
            'quantite': 'Quantité',
        }


# Formsets pour gérer plusieurs pièces à la fois
from django.forms import inlineformset_factory

PieceRechangeFormSet = inlineformset_factory(
    Intervention,
    PieceRechange,
    form=PieceRechangeForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class DirectionForm(forms.ModelForm):
    """Formulaire de création/modification de direction"""
    class Meta:
        model = Direction
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BureauForm(forms.ModelForm):
    """Formulaire de création/modification de bureau"""
    class Meta:
        model = Bureau
        fields = ['nom', 'direction']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-select'}),
        }


class CategorieEquipementForm(forms.ModelForm):
    """Formulaire de création/modification de catégorie"""
    class Meta:
        model = CategorieEquipement
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FiltreDemandeForm(forms.Form):
    """Formulaire de filtrage des demandes (Admin)"""
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + list(DemandeMaintenance.STATUT_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    urgence = forms.ChoiceField(
        choices=[('', 'Toutes les urgences')] + list(DemandeMaintenance.URGENCE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    technicien = forms.ModelChoiceField(
        queryset=User.objects.filter(role='TECHNICIEN', is_active=True),
        required=False,
        empty_label='Tous les techniciens',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    code_equipement = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: PC-001'})
    )
    categorie = forms.ModelChoiceField(
        queryset=CategorieEquipement.objects.all(),
        required=False,
        empty_label='Toutes les catégories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class FiltreEquipementForm(forms.Form):
    """Formulaire de filtrage des équipements (Admin)"""
    code_equipement = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: PC-001'})
    )
    marque = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par marque...'})
    )
    categorie = forms.ModelChoiceField(
        queryset=CategorieEquipement.objects.all(),
        required=False,
        empty_label='Toutes les catégories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    bureau = forms.ModelChoiceField(
        queryset=Bureau.objects.all(),
        required=False,
        empty_label='Tous les bureaux',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class FichierInterventionForm(forms.ModelForm):
    """Formulaire d'ajout de fichier à une intervention"""
    class Meta:
        model = FichierIntervention
        fields = ['fichier', 'type_fichier', 'description']
        widgets = {
            'fichier': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
            'type_fichier': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'placeholder': 'Description optionnelle du fichier...'
            }),
        }
        labels = {
            'fichier': 'Sélectionner un fichier',
            'type_fichier': 'Type de document',
            'description': 'Description',
        }
    
    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if fichier:
            # Vérifier la taille (5MB max)
            if fichier.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La taille du fichier ne doit pas dépasser 5MB.')
            
            # Vérifier l'extension
            ext = fichier.name.split('.')[-1].lower()
            extensions_autorisees = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
            if ext not in extensions_autorisees:
                raise forms.ValidationError(
                    f'Type de fichier non autorisé. Extensions acceptées : {", ".join(extensions_autorisees)}'
                )
        
        return fichier


# Formset pour gérer plusieurs fichiers à la fois


FichierInterventionFormSet = inlineformset_factory(
    Intervention,
    FichierIntervention,
    form=FichierInterventionForm,
    extra=3,  # 3 champs de fichiers vides par défaut
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class FiltreLogForm(forms.Form):
    """Formulaire de filtrage des logs"""
    utilisateur = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=False,
        empty_label='Tous les utilisateurs',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    action = forms.ChoiceField(
        choices=[('', 'Toutes les actions')] + LogAction.TYPE_ACTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    recherche = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher dans les détails...'})
    )

class FiltreInterventionForm(forms.Form):
    """Formulaire de filtrage des interventions"""
    technicien = forms.ModelChoiceField(
        queryset=User.objects.filter(role='TECHNICIEN', is_active=True),
        required=False,
        empty_label='Tous les techniciens',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    code_equipement = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: PC-001'})
    )
    type_reparation = forms.ChoiceField(
        choices=[('', 'Tous les types')] + Intervention.TYPE_REPARATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )