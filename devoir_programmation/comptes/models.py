from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.translation import ugettext_lazy as _
class CompteManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Email est obligatoir")
        if not username :
            raise ValueError("Nom d'utilisateur  est obligatoir")
        
        user = self.model( email=email,username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
         


class Compte(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name="email")
    username = models.CharField(max_length=30,unique=True)
    type_cmp = models.IntegerField(verbose_name="type_cmp")
    is_supperuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)
    objects = CompteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','type_cmp']


    def __str__(self):
        return self.username
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

