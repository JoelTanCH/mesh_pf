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
    path('summaryReport/', views.summaryReport, name='summaryReport'),
    path('summaryReport/healthReportInfo/', views.healthReportInfo, name='healthReportInfo'),
    path('healthReportInfo/draftGeneratedPage/', views.draftGeneratedPage, name='draft generated page'),
    path('healthReportInfo/draftGenerationFailed/', views.draftGenerationFailed, name='draft generation failed'),
    path('summaryReport/healthReportInfo/invalidGeneration/', views.invalidGeneration, name='invalidGeneration'),
    path('summaryReport/sendReportSelection', views.send_selection, name='send-selection'),
    path('summaryReport/healthReportInfo/sendNewReportSelection', views.send_new_selection, name='send-new-selection'),
    path('setting/', views.recTemplateInfo, name='settings page'),
    path('summaryReport/healthReportInfo/downloadcsv/', views.downloadcsv, name='downloadcsv'),
    path('ok/', views.ok, name='ok')
] 
