from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('updateRecommendations/', views.updateRecommendations, name='updateRecommendations'),
    path('upload/',views.upload, name='upload'),
    path('dump/',views.dump, name='dump'),
    #path('base/', views.base, name='base page'), 
    path('', views.home, name='home page'), 
    path('setting/', views.recTemplateInfo, name='settings page'),
    path('summaryReport/', views.summaryReport, name='summary report page'),
    path('ok/', views.ok, name='ok')
] 
