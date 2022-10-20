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


def recTemplateInfo(response):
    template_info = [
        ["Alcohol","Health professionals recognise that it may not be possible to practise total abstinence for individuals who already consume alcohol regularly. However it is advisable to adhere to established recommendations on consumption limits ie: 1 unit of alcohol per day for females, 2 units of alcohol per day for males."],
        ["Smoking","Complete cessation is always recommended by health professionals. The trajectory to this end-goal should be gradual and progressive. Individuals may consult their health professional or seek a counsellour's advice at QuitLine 1800 438 2000."],
        ["Weight","Health professionals recommend regular exercise of at least 3 times weekly for 30 mins per session (moderate-intensity aerobic physical activity). Reduce consumption of foodstuffs high in carbohydrate content, saturated and trans-fats"],
        ["Blood Pressure","Health professionals recommend regular exercise of at least 3 times weekly for 30 mins per session (moderate-intensity aerobic physical activity). Reduce consumption of diet high in salt content. A review of the individual's blood pressure is advised in any case of concern."],
        ["Diabetes","Health professionals recommend regular exercise of at least 3 times weekly for 30 mins per session  (moderate-intensity aerobic physical activity). Reduce consumption of carbohydrates (e.g. rice, noodles, bread), sugary and fatty foods. Increase consumption of low- GI/high-fibre foods like vegetables and brown rice at most meals if possible. A baseline review of the individual's test results is advised."],
        ["Lipids","Health professionals recommend regular exercise of at least 3 times weekly for 30 mins per session  (moderate-intensity aerobic physical activity). Reduce consumption of foodstuffs high in saturated and trans-fats. A baseline review of the individual's test results is advised."]
    ]
    
    return render(response,"setting.html",{
        "template_info":template_info
    })

def ok(response):
    return render(response,"")