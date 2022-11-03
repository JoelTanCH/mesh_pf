from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helper import *
from datetime import datetime
import requests, PyPDF2
from io import BytesIO


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
    #get all batches under all corporates under this healthcare provider
    all_batches = []
    all_batch_ids = []
    for corporate in corporates:
        batchlist = get_batch_list("Parkway Health", corporate[1])
        batch_names = [x['name'] for x in batchlist]
        batch_ids = [str(x['_id']) for x in batchlist]
        all_batches.append(batch_names)
        all_batch_ids.append(batch_ids)

    print('all_corporate_batches')
    print(all_batches)
    print(all_batch_ids)
    #just putting in fake data
    all_batches[1] = ['Batch E (2020,Dec)', 'Batch A (2020, Jan)', 'Batch D (2020, Oct)', 'Batch B (2020, Mar)', 'Batch C (2020, Jul)']


    return render(response, "summaryReport.html", 
    {
        "report_info": report_info,
        "corporate_infos": corporates,
        "corporate_names": corporate_names,
        "corporate_batches": all_batches,
        "corporate_batches_ids": all_batch_ids,
        "nBatches": n_batches
      
    })

@api_view(["POST"])
@csrf_exempt
def update_nbatches(response):
    # if response == 'post':
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
    return redirect('healthReportInfo')

@api_view(["POST"])
@csrf_exempt
def send_selection(response):
    print('response data for send_selection')
    corp_name = response.data.get('corp_name', None)
    response.session["corp_name"] = corp_name
    report_title = response.data.get('report_title', None)
    response.session["corp_report_title"] = report_title
    report_type = response.data.get('report_type', None)
    response.session["corp_report_type"] = report_type
    report_template = response.data.get('report_template', None)
    batches_to_include = response.data.get('batches_to_include', None)
    response.session["corp_report_batches"] = batches_to_include
    clinic_personnel = response.data.get('clinic_personnel', None)
    idx_selected = response.data.get('idx_selected', None)
    batches_to_include_obj_ids = response.data.get('batches_to_include_obj_ids', None)
    arr_batchid = list(batches_to_include_obj_ids.split(','))
    arr_objectbatchid = []
    for batchid in arr_batchid:
        objectid = ObjectId(batchid)
        # objectid = 'Object(' + batchid +')'
        arr_objectbatchid.append(objectid)
    print('type of objectbatchid')
    print(type(arr_objectbatchid))
    print(batches_to_include_obj_ids) #remeember to convert back to ObjectId (now is string)
    corporate_info = get_corporate_list('Parkway Health')
    corporates = [[corp_dic['name'], corp_dic['_id']] for corp_dic in corporate_info]
    corp_id = corporates[int(idx_selected)][1]
    timestamp_gen = datetime.now()
    dict_report = {
        'organization': 'Parkway health',
        'corporateid': corp_id, 
        'name': corp_name, 
        'batches': arr_objectbatchid, 
        'report_template': report_template, 
        'report_type': report_type, 
        'created_by': {'name': clinic_personnel, 'created_time': timestamp_gen} 
    }
    print(dict_report)
    generate_corp_report(dict_report)
    pdf_path = 'https://apps.who.int/iris/bitstream/handle/10665/349091/WHO-EURO-2021-2661-42417-58838-eng.pdf'
    #return HttpResponseRedirect(reverse('healthReportInfo'))
    return render(response, 'healthReportInfo.html',{
        'pdf_path': pdf_path
    } )
    
    

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
    url = "https://apps.who.int/iris/bitstream/handle/10665/349091/WHO-EURO-2021-2661-42417-58838-eng.pdf"
    response = requests.get(url)
    my_raw_data = response.content
    with BytesIO(my_raw_data) as data:
        read_pdf = PyPDF2.PdfFileReader(data)
    num_pages = read_pdf.getNumPages()
    print('num pages:',num_pages)
    return render(response, "healthReportInfo.html", 
    {
        "log_info" : log_info,
        'pdf_path': pdf_path,
        'corp_name' : response.session["corp_name"],
        'corp_report_title' : response.session["corp_report_title"],
        'corp_report_type' : response.session["corp_report_type"],
        'corp_report_batches': response.session["corp_report_batches"]

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