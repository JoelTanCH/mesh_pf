from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def home(response):
    return HttpResponse("<h1> HOME </>")

def base(response):
    return render(response, "base.html", {})