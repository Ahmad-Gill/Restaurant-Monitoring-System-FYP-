from django.urls import path
from . import views
from .views import customer_waiting_time_for_order
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # main path 
    path('', views.main, name='main'),
    path('analytics/', views.analytics_review, name='analytics'),
    path('analytics_table/', views.analytics_tables, name='analytics_table'),
    path('checks/', views.checks, name='checks'),

    # Categories
    path('categories/', views.categories, name='categories'),

    #Auth
     path('login/', views.login, name='login'),
     path("logoutUser/", views.logoutUser, name='logoutUser'),

     # Categories
       path('waiting-time-for-order/', views.customer_waiting_time_for_order, name='waiting_time_for_order'),
       path('waiting-time-for-order_Visualization/', views.customer_waiting_time_for_order_Visualization, name='waiting_time_for_order_Visualization'),  

  path('select-video/', views.select_video, name='select_video'),  # URL for the Select Video page
     # Sample PY file 
   path('preprocessing/', views.preprocessing, name='preprocessing'),
    path('preprocessing_1', views.preprocessing_1, name='preprocessing_1'),  # Map the URL to your view
    path('preprocessing_2/', views.preprocessing_2, name='preprocessing_2'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)