from django.urls import path
from . import views

urlpatterns = [
    #path('base/', views.base, name='base page'), 
    path('', views.home, name='home page'), 
    path('setting/', views.setting, name='settings page'),
    path('summaryReport/', views.summaryReport, name='summary report page'),
    path('healthReportInfo/', views.healthReportInfo, name='health-report-info'),
    path('healthReportInfo/draftGeneratedPage/', views.draftGeneratedPage, name='draft generated page'),
    path('healthReportInfo/draftGenerationFailed/', views.draftGenerationFailed, name='draft generation failed'),
    path('healthReportInfo/invalidGeneration/', views.invalidGeneration, name='invalid generation'),
   path('update_nbatches', views.update_nbatches, name='update-nbatches'),
   path('summaryReport/get_nbatches', views.get_nbatches, name='get-nbatches'),
]
