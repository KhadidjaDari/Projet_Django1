from django.db import models
# Create your models here.
PROMOTION=(('L2', 'L2'),('L3', 'L3'),('M1GL','M1GL'),('M2GL','M2GL'),('M1RSD','M1RSD'),('M2RSD','M2RSD'),('M1MID','M1MID'),('M2MID','M2MID'),('M1SIC','M1SIC'),('M2SIC','M2SIC'))
class Enseignants(models.Model):
    user = models.ForeignKey(to='comptes.Compte', on_delete=models.CASCADE)
    nom = models.CharField(max_length=50,blank=True,null=True)
    prenom = models.CharField(max_length=50,blank=True,null=True)
    grade=models.CharField(max_length=50,blank=True,null=True)
    date_naiss = models.DateField(blank=True,null=True)
    avatar = models.ImageField(null=True, blank=True,upload_to="avatars")
class Categorie(models.Model):
    nom = models.CharField(max_length=50)
    promo = models.CharField(max_length=6,choices=PROMOTION)
class Devoirs(models.Model):
    titre = models.CharField(max_length=100)
    module = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    DEV = (('sommative', 'sommative'),('formative', 'formative'))
    type_dev = models.CharField(max_length=10,choices=DEV)
    date_fin = models.DateField()
    date_dep = models.DateField(auto_now=True)
    fichier = models.FileField(upload_to='devoir')
    id_ens = models.ForeignKey(Enseignants, on_delete=models.CASCADE)
class Etudiant(models.Model):
    user = models.ForeignKey(to='comptes.Compte', on_delete=models.CASCADE)
    nom = models.CharField(max_length=50,blank=True,null=True)
    prenom = models.CharField(max_length=50,blank=True,null=True)
    promo = models.CharField(max_length=6,choices=PROMOTION)
    date_naiss = models.DateField(blank=True,null=True)
    avatar = models.ImageField(null=True, blank=True,upload_to="avatars")
class Soumission(models.Model):
    id_etud = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    id_dev = models.ForeignKey(Devoirs, on_delete=models.CASCADE)
    note = models.FloatField()
    date_soumission = models.DateField(auto_now=True)
    solution = models.FileField(upload_to='solutions')