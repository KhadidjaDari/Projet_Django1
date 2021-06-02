# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views
from comptes import views as v
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('reg',v.register,name='reg'),
    path('log',v.login_comp,name='login'),
    path('logout',v.logout_cmp,name='logout'),
    path('ss',views.swwet,name="ss"),
    path('dashbord',views.dashboard,name="dashboard"),
    path('ajouter_devoir',views.AjouterDevoir,name='ajouter_devoir'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]