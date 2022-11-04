from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.urls import reverse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helper import *
from datetime import datetime
import requests, PyPDF2
from io import BytesIO
import time
import re
from PIL import Image
import json
import os

from .forms import RecommendationsForm, UploadFileForm

summary_ref_filepath = "C:/Users/joelt/OneDrive/Documents/GitHub/mesh_pf/mysite/main/executiveSummaryReference.json"

# Create your views here.

def updateSummaryReference(new_data_dict):
    key_mapping = {
    "Alcohol": ["habits-alcoholIntake"],
    "Weight": ["bodyMassIndex", "bodyMassIndexObese"],
    "Blood Pressure": ["systolicBloodPressure", "diastolicBloodPressure"],
    "Smoking": ["habits-smoking"],
    "Lipids": ["totalCholesterol", "lowDensityLipidCholesterol", "highDensityLipidCholesterol", "triglycerides"],
    "Diabetes": ["glucose"]
}
    with open(summary_ref_filepath, "r") as fp:
        data = json.load(fp)

    for k, v in new_data_dict.items():
        update_list = key_mapping[k]
        for item in update_list:
            data[item]["recommendations"] = v[0].rstrip()

    with open(summary_ref_filepath, "w", encoding='utf-8') as ufp:
        json.dump(data, ufp, ensure_ascii=False, indent=4)



def updateRecommendations(request):
    print("REQUEST = ", request.POST)

    if request.POST:
        #form = RecommendationsForm(request.POST, request.FILES)
        updateSummaryReference(dict(request.POST))
        # Alcohol = form['Alcohol'].value()
        # Weight =form['Weight'].value()
        # Blood_Pressure = form['Blood_Pressure'].value()
        # Smoking = form['Smoking'].value()
        # Lipids = form['Lipids'].value()
        # Diabetes = form['Diabetes'].value()

        # print("alc: ", Alcohol)

        return JsonResponse({"success":True})
    return JsonResponse({"success": False})



def dump(request):
    print("REQUEST = ", request)
    if request.FILES:
        return JsonResponse({"success":True})
    return JsonResponse({"success": False})


def upload(request):
    print("REQUEST = ", request)
    print(request.FILES)
    if request.FILES:
        form = UploadFileForm(request.POST, request.FILES)
        print("form: ", form)
        fontType = form['font'].value()
        print("FONTTYPE = ", fontType)
        #for f in request.FILES:
        #    print(f)    header, frontpage 
        print("REQUEST = ", request)
        print("FILES: ", request.FILES)
        header_name = request.FILES['header'] # gives name 
        header_type = request.FILES['header'].content_type.split('/')[1]
        frontpage_name = request.FILES['frontpage']
        frontpage_type = request.FILES['frontpage'].content_type.split('/')[1]
        upload_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        newpath = f'./uploads/{upload_time})'
        os.makedirs(newpath)
        print(type(request.FILES['header'])) #gives django core files uploaded file obkect
        #print(request.FILES['header'].file) #gives io.bytesIO
        imgHeader = Image.open(header_name)
        imgHeader.save(f"{newpath}/header_{header_name}",format=header_type)
        imgFrontpage = Image.open(frontpage_name)
        imgFrontpage.save(f"{newpath}/frontpage_{frontpage_name}",format=frontpage_type)
        return JsonResponse({"success":True})
    
    return JsonResponse({"success": False})

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
    response.session["corp_report_template"] = report_template
    batches_to_include = response.data.get('batches_to_include', None)
    response.session["corp_report_batches"] = batches_to_include
    clinic_personnel = response.data.get('clinic_personnel', None)
    response.session["clinic_personnel"] = clinic_personnel
    idx_selected = response.data.get('idx_selected', None)
    batches_to_include_obj_ids = response.data.get('batches_to_include_obj_ids', None)
    response.session['batches_to_include_obj_ids'] = batches_to_include_obj_ids
    response.session["idx_selected"] = idx_selected
    return render(response, 'healthReportInfo.html', {})

def setting(response):
    props = {}
    return render(response, "setting.html", props)

@api_view(["GET", 'POST'])
def healthReportInfo(response):
    print('healthReportInfo called')
    timestamp_gen = datetime.now()
    batches_to_include_obj_ids = response.session['batches_to_include_obj_ids']
    arr_batchid = list(batches_to_include_obj_ids.split(','))
    arr_objectbatchid = []
    for batchid in arr_batchid:
        objectid = ObjectId(batchid)
        arr_objectbatchid.append(objectid)
    print(type(objectid))
    print(objectid)
    corporate_info = get_corporate_list('Parkway Health')
    corporates = [[corp_dic['name'], corp_dic['_id']] for corp_dic in corporate_info]
    corp_id = corporates[int(response.session['idx_selected'])][1]
    url = "https://apps.who.int/iris/bitstream/handle/10665/349091/WHO-EURO-2021-2661-42417-58838-eng.pdf"
    # url = "https://docs.google.com/file/d/13IHnY7QsRz54qJ5fi61_c6Kfi7m2g_ul/preview"
    
    req_response = requests.get(url)
    my_raw_data = req_response.content
    with BytesIO(my_raw_data) as data:
        read_pdf = PyPDF2.PdfFileReader(data)
        num_pages = read_pdf.getNumPages()
    dict_report = {
        'organization': 'Parkway health',
        'corporateid': corp_id, 
        'name': response.session['corp_name'], 
        'batches': arr_objectbatchid, 
        'report_template': response.session['corp_report_template'], 
        'report_type': response.session['corp_report_type'], 
        'created_by': {'name': response.session['clinic_personnel'], 'created_time': timestamp_gen} 
    }
    print('dict_report')
    print(dict_report)
    last_gen_name, last_gen_time, inserted_doc_id = generate_corp_report(dict_report)
    print('inserted doc id type')
    print(type(inserted_doc_id))
    audit_trail = retrieve_audit_trail(inserted_doc_id)
    log_info = []
    for dict in audit_trail:
        log = [dict['datetime'], dict['action'], dict['user']]
        log_info.append(log)
    log_info = sorted(log_info, key= lambda x: x[0])
    print(log_info)
    
    return render(response, "healthReportInfo.html", 
    {
        "log_info" : log_info,
        'pdf_path': url,
        "num_pages": num_pages,
        'latest_generated_by' : last_gen_name,
        'latest_generated_timestamp': last_gen_time,
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

def recTemplateInfo(response):

    with open(summary_ref_filepath, "r") as fp:
        data = json.load(fp)

    key_mapping = {
        "Alcohol": "habits-alcoholIntake",
        "Smoking": "habits-smoking",
        "Weight": "bodyMassIndex",
        "Blood Pressure": "systolicBloodPressure",
        "Diabetes": "glucose",
        "Lipids": "totalCholesterol"
    }

    template_info = [[k, " ".join(data[v]["recommendations"])] for k, v in key_mapping.items()]
    return render(response,"setting.html",{
        "template_info":template_info
    })

def ok(response):
    return render(response,"")    
