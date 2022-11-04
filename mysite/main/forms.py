from operator import truediv
from django import forms 
from .models import Document

class UploadFileForm(forms.Form):

    frontpage = forms.ImageField()
    header = forms.ImageField()
    font = forms.CharField(max_length=250)

class RecommendationsForm(forms.Form):
    Alcohol = forms.CharField(max_length=500)
    Weight = forms.CharField(max_length=500)
    Blood_Pressure = forms.CharField(max_length=500)
    Smoking = forms.CharField(max_length=500)
    Lipids = forms.CharField(max_length=500)
    Diabetes = forms.CharField(max_length=500)