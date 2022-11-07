from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.urls import reverse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helper import *
from datetime import datetime
import pytz
import requests, PyPDF2
from io import BytesIO
import time
import re
from PIL import Image
import json
import os
from .export_csv import *
from .forms import RecommendationsForm, UploadFileForm

summary_ref_filepath = "/Users/jiaxuan/Desktop/BT4103/pfe/mysite/main/executiveSummaryReference.json"

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
        # datetime.strftime(datetime.now(pytz.timezone('Asia/Singapore')), "%Y-%m-%d %H:%M:%S")
        upload_time = datetime.now(pytz.timezone('Asia/Singapore')).strftime("%Y_%m_%d-%I_%M_%S_%p")
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

    reportdata = retrieve_corporate_report_data('Parkway health')
    print('REPORTDATA')
    print(reportdata)
    reportarr = []
    # str array is to display batches as strings in the summaryReport table
    reportarrstr = []
    for dict in reportdata:
        arr = [0]*4
        arr[0] = dict['report_title']
        arr[1] = dict['batches']
        arr[2] = dict['last_generated_time']
        arr[3] = dict['status']
        reportarr.append(arr)
        arrstr = [0]*4
        arrstr[0] = dict['report_title']
        sl = str(dict['batches'])
        sl = sl.replace("]", "")
        sl = sl.replace("[", "")
        arrstr[1] = sl
        arrstr[2] = dict['last_generated_time']
        arrstr[3] = dict['status']
        reportarrstr.append(arrstr)
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
        "report_info": reportarr,
        "report_info_str": reportarrstr,
        "corporate_infos": corporates,
        "corporate_names": corporate_names,
        "corporate_batches": all_batches,
        "corporate_batches_ids": all_batch_ids,
        "nBatches": n_batches
      
    })

@api_view(["GET"])
def downloadcsv(request):
    try:
        myfile = open('./temp/validated_data_with_base_units.csv')
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=validated_data_with_base_units.csv'
        return response
    except:
        response = HttpResponse()
        response.status_code = 404
        return response

@api_view(["GET"])
def invaliddownloadcsv(request):
    try:
        myfile = open('./temp/validated_data_with_base_units.csv')
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=validated_data_with_base_units.csv'
        return response
    except:
        response = HttpResponse()
        response.status_code = 404
        return response

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
    response.session['audit_log_id'] = 0
    return render(response, 'healthReportInfo.html', {})

@api_view(["POST"])
@csrf_exempt
def send_new_selection(response):
    print('response data for send_new_selection')
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
    audit_log_id = response.data.get('audit_log_id', None)
    response.session['audit_log_id'] = audit_log_id
    print('audit_log_id is:')
    print(audit_log_id)
    print('corp name is:')
    print(corp_name)

    # updating audit trail
    timestamp_gen = datetime.now(pytz.timezone('Asia/Singapore'))
    batches_to_include_obj_ids = response.session['batches_to_include_obj_ids']
    arr_batchid = list(batches_to_include_obj_ids.split(','))
    arr_objectbatchid = []
    for batchid in arr_batchid:
        print('BATCH ID')
        print(batchid)
        objectid = ObjectId(batchid)
        arr_objectbatchid.append(objectid)
    corporate_info = get_corporate_list('Parkway Health')
    corporates = [[corp_dic['name'], corp_dic['_id']] for corp_dic in corporate_info]
    corp_id = corporates[int(response.session['idx_selected'])][1]

    dict_report = {
        'organization': 'Parkway health',
        'corporateid': corp_id, 
        'report_title': response.session['corp_report_title'],
        'name': response.session['corp_name'], 
        'batches': arr_objectbatchid, 
        'report_template': response.session['corp_report_template'], 
        'report_type': response.session['corp_report_type'], 
        'created_by': {'name': response.session['clinic_personnel'], 'created_time': timestamp_gen} 
    }
    print('dict_report')
    print(dict_report)
    last_gen_name, last_gen_time, inserted_doc_id = generate_corp_report(dict_report, ObjectId(audit_log_id))
    print('inserted doc id after generating again at send new selection')
    print(inserted_doc_id)
    audit_trail = retrieve_audit_trail(inserted_doc_id)
    return render(response, 'healthReportInfo.html', {})

def setting(response):
    props = {}
    return render(response, "setting.html", props)

@api_view(["GET", 'POST'])
def healthReportInfo(response):
    # information required to render healthReportInfo page
    print('healthReportInfo called')
    timestamp_gen = datetime.now(pytz.timezone('Asia/Singapore'))
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
    url = "https://res.cloudinary.com/dvyhz42sn/image/upload/v1667807654/bt4103Demo/DARA-Corporate-2022-11-04-12-23-8462a4ca_n8efmz.pdf"

    with BytesIO(requests.get(url).content) as data:
        read_pdf = PyPDF2.PdfFileReader(data)
        num_pages = read_pdf.getNumPages()
    dict_report = {
        'organization': 'Parkway health',
        'corporateid': corp_id, 
        'report_title': response.session['corp_report_title'],
        'name': response.session['corp_name'], 
        'batches': arr_objectbatchid, 
        'report_template': response.session['corp_report_template'], 
        'report_type': response.session['corp_report_type'], 
        'created_by': {'name': response.session['clinic_personnel'], 'created_time': timestamp_gen} 
    }
    if response.session['audit_log_id'] == 0:
        last_gen_name, last_gen_time, inserted_doc_id = generate_corp_report(dict_report)
    else:
        inserted_doc_id = ObjectId(response.session['audit_log_id'])
        last_gen_name = response.session['clinic_personnel']
        last_gen_time = timestamp_gen

    audit_trail = retrieve_audit_trail(inserted_doc_id)
    log_info = []
    for dict in audit_trail:
        log = [dict['datetime'], dict['action'], dict['user']]
        log_info.append(log)
    log_info = sorted(log_info, key= lambda x: x[0])
    print(log_info)

    # info required to download csv
    patient_records_df, indicators_no_units, error = export_base_csv(arr_objectbatchid,'DBS', 'Parkway Health' )
    
    # info required to customised modal again
    corporate_info = get_corporate_list('Parkway Health')
    corporates = [[corp_dic['name'], corp_dic['_id']] for corp_dic in corporate_info]
    corporate_names = [corp_dic['name'] for corp_dic in corporate_info]

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
        'corp_report_batches': response.session["corp_report_batches"],
        'pdf_gen_error' : error,
        "corporate_infos": corporates,
        "corporate_names": corporate_names,
        "corporate_batches": all_batches,
        "corporate_batches_ids": all_batch_ids,
        "audit_log_id": inserted_doc_id
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
