from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from comptes.models import Compte
from comptes.forms import RegistrationFormAdmin, UserChangeForm


class CompteAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = RegistrationFormAdmin

    list_display = ('email', 'username', 'type_cmp', 'is_staff',  'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('username', 'type_cmp',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2',)}),
        ('Personal info', {'fields': ('username', 'type_cmp',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'username', 'type_cmp')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Compte, CompteAdmin)