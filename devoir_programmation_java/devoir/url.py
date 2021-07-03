# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views
from comptes import views as v
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('reg',v.register,name='reg'),
    path('log',v.login_comp,name='login'),
    path('logout',v.logout_cmp,name='logout'),
    path('ss',views.swwet,name="ss"),
    path('dashbord',views.dashboard,name="dashboard"),
    path('ajouter_devoir',views.AjouterDevoir,name='ajouter_devoir'),
    path('Profil',views.Profil,name='Profil'),
    path('ModifierInfo',views.ModifierInfo,name='ModifierInfo'),
    path('ModifierAvatar',views.ModifierAvatar,name='ModifierAvatar'),
    path('ListDevoir',views.ListDevoir,name='ListDevoir'),
    path('AfficheDevoir/<int:id_dev>',views.AfficheDevoir,name='AfficheDevoir'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
