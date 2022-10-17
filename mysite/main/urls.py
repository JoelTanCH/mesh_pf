from django.urls import path

from . import views

urlpatterns = [
    #path('base/', views.base, name='base page'), 
    path('', views.home, name='home page'), 
    path('setting/', views.recTemplateInfo, name='settings page'),
    path('summaryReport/', views.summaryReport, name='summary report page')
]
