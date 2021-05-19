# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from . import views

urlpatterns = [
    path('reg',views.register,name='reg'),
    path('login',views.login,name='login'),
    path('logout',views.login,name='logout'),

]