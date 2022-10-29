from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helper import *
import PyPDF2
from datetime import datetime


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
    corporate_info = get_corporate_list('Parkway Health')
    corporates = [[corp_dic['name'], corp_dic['_id']] for corp_dic in corporate_info]
    corporate_names = [corp_dic['name'] for corp_dic in corporate_info]
    print('no. of corporates', len(corporates))
    print(corporates)
    # all_corporate_batches = []
    # for i in range(len(corporates)):
    #     all_corporate_batches.append(get_batch_list('Parkway Health', corporates[i][1]))
    print(corporates[2][1])
    batchlist = get_batch_list('Parkway Health', corporates[2][1])
    batch_names = [[x['name'], x['_id']] for x in batchlist]
    print('all_corporate_batches')
    print(batch_names)
    # corp_batches_arr = [[str(batch['_id']), batch['name']] for batch in all_corporate_batches]
    # print(corp_batches_arr)

    return render(response, "summaryReport.html", 
    {
        "report_info": report_info,
        "corporate_infos": corporates,
        "corporate_names": corporate_names,
        "corporate_batches": batch_names,
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

@api_view(["POST"])
@csrf_exempt
def send_selection(response):
    print('response data for send_selection')
    corp_name = response.data.get('corp_name', None)
    print(corp_name)
    report_title = response.data.get('report_title', None)
    print(report_title)
    report_type = response.data.get('report_type', None)
    print(report_type)
    report_template = response.data.get('report_template', None)
    print(report_template)
    batches_to_include = response.data.get('batches_to_include', None)
    print(batches_to_include)
    clinic_personnel = response.data.get('clinic_personnel', None)
    print(clinic_personnel)
    idx_selected = response.data.get('idx_selected', None)
    print(idx_selected)
    corporate_info = get_corporate_list('Parkway Health')
    corporates = [[corp_dic['name'], corp_dic['_id']] for corp_dic in corporate_info]
    corp_id = corporates[int(idx_selected)][1]
    print(corp_id)
    timestamp_gen = datetime.now()
    print(timestamp_gen)
    # return HttpResponseRedirect(reverse('healthReportInfo'))
    return redirect('healthReportInfo')
    
    

def get_nbatches(response):
    if response == 'GET':
        return render(response, 'summaryReport.html', {
            "nBatches" : n_batches
        })
    

def setting(response):
    props = {}
    return render(response, "setting.html", props)

@api_view(["GET", 'POST'])
def healthReportInfo(response):
    log_info = [
        ['2021.10.01 13:23', 'Email Sent', 'Chua Li Li'],
        ['2021.10.01 13:23', 'PDF generation', 'Chua Li Li'],
        ['2021.06.18 08:46', 'Email Sent', 'Linda Tan'],
        ['2021.06.18 08:46', 'PDF generation', 'Linda Tan'],
        ['2021.06.18 08:46', 'PDF generation', 'Linda Tan'],
    ]
    pdf_path = '/Users/jiaxuan/Desktop/BT4103/pfe/mysite/temp_pdf/WHO-EURO-2021-2661-42417-58838-eng.pdf'
    file = open(pdf_path, 'rb')
    readpdf = PyPDF2.PdfFileReader(file)
    total_pages = readpdf.numPages
    return render(response, "healthReportInfo.html", 
    {
        "log_info" : log_info,
        'pdf_path': pdf_path,
        'total_pages': total_pages
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