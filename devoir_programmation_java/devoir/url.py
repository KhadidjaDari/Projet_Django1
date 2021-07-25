# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path,include
from . import views
from comptes import views as v
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('reg',v.register,name='reg'),
    path('log',v.login_comp,name='login'),
    path('logout',v.logout_cmp,name='logout'),
    path('dashbord',views.dashboard,name="dashboard"),
    path('ajouter_devoir',views.AjouterDevoir,name='ajouter_devoir'),
    path('Profil',views.Profil,name='Profil'),
    path('ModifierInfo',views.ModifierInfo,name='ModifierInfo'),
    path('ModifierAvatar',views.ModifierAvatar,name='ModifierAvatar'),
    path('ListDevoir',views.ListDevoir,name='ListDevoir'),
    path('AfficheDevoir/<int:id_dev>',views.AfficheDevoir,name='AfficheDevoir'),
    path('Soumission_Etud/<int:id_dev>/<int:id_etud>',views.Soumission_Etud,name='Soumission_Etud'),
    path('listEtudiant',views.listEtudiant,name='listEtudiant'),
    path('MesDevoir',views.MesDevoir,name='MesDevoir'),
    path('SupprimerDevoir/<int:id_dev>',views.SupprimerDevoir,name='SupprimerDevoir'),
    path('ModifierDevoir/<int:id_dev>',views.ModifierDevoir,name='ModifierDevoir'),
    path('QuiFaitDevoir/<int:id_dev>',views.QuiFaitDevoir,name='QuiFaitDevoir'),
    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    #path('dashboard/', views.dashboard, name='dashboard'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
