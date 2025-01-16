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
     path('cheff-and-people/', views.cheff_and_people, name='cheff_and_people'),
      path('final_chef_preprocessing/', views.final_chef_preprocessing1, name='final_chef_preprocessing1'),
       path('final_chef_preprocessing2/', views.final_chef_preprocessing2, name='final_chef_preprocessing2'),

      


    #Auth
     path('login/', views.login, name='login'),
     path("logoutUser/", views.logoutUser, name='logoutUser'),

     # Categories
       path('waiting-time-for-order/', views.customer_waiting_time_for_order, name='waiting_time_for_order'),
       path('waiting-time-for-order_Visualization/', views.customer_waiting_time_for_order_Visualization, name='waiting_time_for_order_Visualization'),  

  path('select-video/', views.select_video, name='select_video'),  
    path('preprocessing_2/', views.preprocessing_2, name='preprocessing_2'),

   path('chef-preprocessing/', views.chef_preprocessing, name='chef_preprocessing'),# URL for the Select Video page
   path('start_preprocessing/', views.start_preprocessing, name='start_preprocessing'),
     # Sample PY file 
   path('preprocessing/', views.preprocessing, name='preprocessing'),
    path('preprocessing_1', views.preprocessing_1, name='preprocessing_1'),  # Map the URL to your view
   
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)