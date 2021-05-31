from django import forms
from django.forms import ModelForm
from .models import *
class Ajouterdevoir(ModelForm):
    id_ens=forms.ModelChoiceField(queryset=Enseignants.objects.only('pk'),widget=forms.HiddenInput())
    module=forms.ModelChoiceField(queryset=Categorie.objects.all())
    class Meta:
        model = Devoirs
        fields=('titre', 'module','type_dev','date_fin','fichier','id_ens')
