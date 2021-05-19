# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    # Matches any html file
    path('reg',views.reg,name='reg'),
    re_path(r'^.*\.*', views.pages, name='pages'),

]