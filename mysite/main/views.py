from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def home(response):
    #return HttpResponse("<h1> HOME PAGE</>")
    props = {}
    return render(response, "home.html", props)

def summaryReport(response):
    report_info = [
        ['SIA Corporate Health Report I', '2021.08.20 08:30', 'Batch A (2021, Jan), Batch B (2021, Mar)'],
        ['ACME Corporate Health Report II', '2020.12.24 15:32', 'Batch D (2020, Oct), Batch E (2020,Dec)'],
        ['ACME Corporate Health Report I', '2020.08.24 12.29', 'Batch A (2020, Jan), Batch B (2020, Mar), Batch C (2020, Jul)']
        ]
    return render(response, "summaryReport.html", {"report_info": report_info})

def setting(response):
    props = {}
    return render(response, "setting.html", props)
