from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from devoir.models import Enseignants,Etudiant
class CompteManager(BaseUserManager):
    def create_user(self,email,username,password=None,type_cmp=None):
        if not email:
            raise ValueError("Email est obligatoir")
        if not username :
            raise ValueError("Nom d'utilisateur  est obligatoir")
        user = self.model( email=email,username=username,type_cmp=type_cmp)
        user.set_password(password)
        user.is_superuser = False
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password=None,type_cmp=None):
        if not email:
            raise ValueError("Email est obligatoir")
        if not username :
            raise ValueError("Nom d'utilisateur  est obligatoir")
        user=self.model(email=email,username=username,is_staff=True,type_cmp='Admin')
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
class Compte(AbstractBaseUser,PermissionsMixin):
    PER=(('Etudiant','Etudiant'),('Enseignant','Enseignant'),('Admin','Admin'))
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name="email")
    username = models.CharField(max_length=30,unique=True)
    type_cmp = models.CharField(max_length=11,choices=PER,help_text="Pour qui voulez-vous créer le compte, si pour l'enseignant, tapez le mot Enseignant")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)
    objects = CompteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','type_cmp']


    def __str__(self):
        return self.username
    def has_module_perms(self,app_label):
       return self.is_superuser
    def has_perm(self,perm,obj=None):
       return self.is_superuser
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

