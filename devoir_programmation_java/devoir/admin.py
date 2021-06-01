from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from devoir.models import Enseignants,Categorie,Etudiant
from comptes.models import Compte
from comptes.forms import RegistrationFormAdmin, UserChangeForm
class CategorieAffiche(admin.ModelAdmin):
    list_display = ('nom', 'promo')
admin.site.register(Categorie,CategorieAffiche)

class CompteAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = RegistrationFormAdmin

    list_display = ('email', 'username', 'type_cmp')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('username', 'type_cmp',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2',)}),
        ('Informations personnelles', {'fields': ('username', 'type_cmp',)}),

    )

    search_fields = ('email', 'username', 'type_cmp')
    ordering = ('email',)
    filter_horizontal = ()
class NotAdd(admin.ModelAdmin):
    list_display = ('nom','prenom' ,'promo')
    exclude=('user',)
    readonly_fields=('nom','prenom','avatar','date_naiss','promo')
    def has_add_permission(self, request):
        return False
class NotAdd2(admin.ModelAdmin):
    list_display = ('nom', 'prenom','grade')
    exclude=('user',)
    readonly_fields=('nom','prenom','avatar','date_naiss','grade')
    def has_add_permission(self, request):
        return False
admin.site.register(Enseignants,NotAdd2)
admin.site.register(Etudiant,NotAdd)
admin.site.register(Compte, CompteAdmin)