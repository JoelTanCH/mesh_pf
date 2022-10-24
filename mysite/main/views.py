from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def home(response):
    #return HttpResponse("<h1> HOME PAGE</>")
    props = {}
    return render(response, "home.html", props)

def summaryReport(response):
    n_batches = 1
    report_info = [
        ['SIA Corporate Health Report I',  'Batch A (2021, Jan), Batch B (2021, Mar)','2021.08.20 08:30', 'Error found'],
        ['ACME Corporate Health Report II', 'Batch D (2020, Oct), Batch E (2020,Dec)', '2020.12.24 15:32', 'Ready' ],
        ['ACME Corporate Health Report I', 'Batch A (2020, Jan), Batch B (2020, Mar), Batch C (2020, Jul)', '2020.08.24 12.29', 'Ready']
        ]

    corporate_ids = [
        'Singapore Airlines Ltd (SIA)',
        'ACME',
        'Company X',
        'Company Y',
        'Company B',
        'NTUC',
        'Govtech',
        'MeshBio'
    ]

    # index of element in corporate_batches corresponds to index of company in corporate_ids
    corporate_batches = [
        ['Batch A (2021, Jan)', 'Batch B (2021, Mar)'],
        ['Batch D (2020, Oct)', 'Batch E (2020,Dec)', 'Batch A (2020, Jan)', 'Batch B (2020, Mar)', 'Batch C (2020, Jul)'],
        ['Batch D (2020, Oct)', 'Batch E (2020,Dec)', 'Batch A (2020, Jan)', 'Batch B (2020, Mar)', 'Batch C (2020, Jul)'],
        ['Batch E (2020,Dec)', 'Batch A (2020, Jan)', 'Batch D (2020, Oct)', 'Batch B (2020, Mar)', 'Batch C (2020, Jul)']
    ]
    print('rendering summaryReport page')
    return render(response, "summaryReport.html", 
    {
        "report_info": report_info,
        "corporate_ids": corporate_ids,
        "corporate_batches": corporate_batches,
        "nBatches": n_batches
      
    })

@api_view(["POST"])
@csrf_exempt
def update_nbatches(response):
    # if response == 'post':
    print('response data is')
    new_nbatch = response.data.get('number_batches', None)
    print(new_nbatch)
    print('updated n_batches:', new_nbatch)
    report_info = [
        ['SIA Corporate Health Report I',  'Batch A (2021, Jan), Batch B (2021, Mar)','2021.08.20 08:30', 'Error found'],
        ['ACME Corporate Health Report II', 'Batch D (2020, Oct), Batch E (2020,Dec)', '2020.12.24 15:32', 'Ready' ],
        ['ACME Corporate Health Report I', 'Batch A (2020, Jan), Batch B (2020, Mar), Batch C (2020, Jul)', '2020.08.24 12.29', 'Ready']
        ]

    corporate_ids = [
        'Singapore Airlines Ltd (SIA)',
        'ACME',
        'Company X',
        'Company Y',
        'Company B',
        'NTUC',
        'Govtech',
        'MeshBio'
    ]

    # index of element in corporate_batches corresponds to index of company in corporate_ids
    corporate_batches = [
        ['Batch A (2021, Jan)', 'Batch B (2021, Mar)'],
        ['Batch D (2020, Oct)', 'Batch E (2020,Dec)', 'Batch A (2020, Jan)', 'Batch B (2020, Mar)', 'Batch C (2020, Jul)'],
        ['Batch D (2020, Oct)', 'Batch E (2020,Dec)', 'Batch A (2020, Jan)', 'Batch B (2020, Mar)', 'Batch C (2020, Jul)'],
        ['Batch E (2020,Dec)', 'Batch A (2020, Jan)', 'Batch D (2020, Oct)', 'Batch B (2020, Mar)', 'Batch C (2020, Jul)']
    ]
    return render(response, "summaryReport.html", 
    {
        "report_info": report_info,
        "corporate_ids": corporate_ids,
        "corporate_batches": corporate_batches,
        "nBatches": new_nbatch
      
    })

def get_nbatches(response):
    if response == 'GET':
        return render(response, 'summaryReport.html', {
            "nBatches" : n_batches
        })
    

def setting(response):
    props = {}
    return render(response, "setting.html", props)

def healthReportInfo(response):
    log_info = [
        ['2021.10.01 13:23', 'Email Sent', 'Chua Li Li'],
        ['2021.10.01 13:23', 'PDF generation', 'Chua Li Li'],
        ['2021.06.18 08:46', 'Email Sent', 'Linda Tan'],
        ['2021.06.18 08:46', 'PDF generation', 'Linda Tan'],
        ['2021.06.18 08:46', 'PDF generation', 'Linda Tan'],
    ]
    return render(response, "healthReportInfo.html", 
    {
        "log_info" : log_info
    })

def draftGeneratedPage(response):
    props = {}
    return render(response, "draftGeneratedPage.html", props)

def draftGenerationFailed(response):
    props = {}
    return render(response, "draftGenerationFailed.html", props)

def invalidGeneration(response):
    props = {}
    return render(response, "invalidGeneration.html", props)