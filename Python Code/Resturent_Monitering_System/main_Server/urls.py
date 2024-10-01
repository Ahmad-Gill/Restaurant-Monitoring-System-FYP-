from django.urls import path
from . import views
from .views import generate_value_view 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # main path 
    path('', views.main, name='main'),

    # Categories
    path('categories/', views.categories, name='categories'),

    #Auth
     path('login/', views.login, name='login'),
     path("logoutUser/", views.logoutUser, name='logoutUser'),


     # Sample PY file 
  path('generate-value/', generate_value_view, name='generate_value'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)