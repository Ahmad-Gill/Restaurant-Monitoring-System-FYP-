from django.urls import path
from . import views
from .views import customer_waiting_time_for_order, generate_value_view 
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

     # Categories
       path('waiting-time-for-order/', views.customer_waiting_time_for_order, name='waiting_time_for_order'),  # This is your URL pattern


     # Sample PY file 
  path('generate-value/', generate_value_view, name='generate_value'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)