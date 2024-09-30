from django.urls import path
from . import views

urlpatterns = [

    # main path 
    path('', views.main, name='main'),

    # Categories
    path('categories/', views.categories, name='categories'),
]