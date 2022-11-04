import re
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from PIL import Image
import json
from datetime import datetime
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
    report_info = [
        ['SIA Corporate Health Report I', '2021.08.20 08:30', 'Batch A (2021, Jan), Batch B (2021, Mar)'],
        ['ACME Corporate Health Report II', '2020.12.24 15:32', 'Batch D (2020, Oct), Batch E (2020,Dec)'],
        ['ACME Corporate Health Report I', '2020.08.24 12.29', 'Batch A (2020, Jan), Batch B (2020, Mar), Batch C (2020, Jul)']
        ]
    return render(response, "summaryReport.html", {"report_info": report_info})


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