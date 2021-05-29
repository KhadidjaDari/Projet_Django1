from django.contrib import admin
from comptes.models import Compte
from devoir.models import Enseignants,Categorie,Etudiant
from comptes.forms import RegistrationForm,CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

admin.site.register(Categorie)
# Register your models here.
"""class CompteUser(admin.ModelAdmin):
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = Compte"""
class NotAdd(admin.ModelAdmin):
    exclude=('user',)
    readonly_fields=('nom','prenom','avatar','date_naiss','promo')
    def has_add_permission(self, request):
        return False
class NotAdd2(admin.ModelAdmin):
    exclude=('user',)
    readonly_fields=('nom','prenom','avatar','date_naiss','grade')
    def has_add_permission(self, request):
        return False
admin.site.register(Compte)
admin.site.register(Enseignants,NotAdd2)
admin.site.register(Etudiant,NotAdd)