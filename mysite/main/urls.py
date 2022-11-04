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
    path('healthReportInfo/invalidGeneration/', views.invalidGeneration, name='invalid generation'),
    path('summaryReport/update_nbatches', views.update_nbatches, name='update_nbatches'),
    path('summaryReport/sendReportSelection', views.send_selection, name='send-selection'),Ï
    path('setting/', views.recTemplateInfo, name='settings page'),
    path('ok/', views.ok, name='ok')
] 
