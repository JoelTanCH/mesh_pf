from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def home(response):
    #return HttpResponse("<h1> HOME PAGE</>")
    props = {}
    return render(response, "home.html", props)

def summaryReport(response):
    props = {}
    return render(response, "summaryReport.html", props)

def setting(response):
    props = {}
    return render(response, "setting.html", props)