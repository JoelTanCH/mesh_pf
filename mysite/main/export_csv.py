from pymongo import MongoClient
import pandas as pd
import os
import json
from data_validation import validate_data
from database import *
from utility import *

from bson.objectid import ObjectId

screen_record_projection = {
    'batchReportId': '$batch_report.id',
    '_id': '$_id',
    'organization': '$organization',
    'Name': '$section.healthhistory.data.name',
    'gender': '$section.healthhistory.data.sex',
    'birthDate': '$section.healthhistory.data.dob',
    'recordDate': {"$dateToString":{"format":"%Y-%m-%d","date":"$firstreporttime"}},
    'labid': '', # where to find this.
    'patientid': '$patientid',
    'packageName': '$package',
    'ethnicity':'$section.healthhistory.data.ethnicity',
    'emailAddress':'$section.healthhistory.data.emailAddress',
    'phoneNumber':'$section.healthhistory.data.phoneNumber',
    'bodyMassIndex':'$section.biometrics.data.bodyMassIndex.value',
    'height':'$section.biometrics.data.height',
    'weight':'$section.biometrics.data.weight',
    'waist': '$section.biometrics.data.waist', # need to check if unit is present
    'diastolicBloodPressure':'$section.bppulse.data.diastolicBloodPressure',
    'systolicBloodPressure':'$section.bppulse.data.systolicBloodPressure',
    'glucose':'$section.laboratory.data.glucose',
    'highDensityLipidCholesterol':'$section.laboratory.data.highDensityLipidCholesterol',
    'lowDensityLipidCholesterol':'$section.laboratory.data.lowDensityLipidCholesterol',
    'totalCholHdlRatio':'$section.laboratory.data.totalCholHdlRatio',
    'totalCholesterol':'$section.laboratory.data.totalCholesterol',
    'triglycerides':'$section.laboratory.data.triglycerides',
    'creatinine':'$section.laboratory.data.creatinine', # no preferred units 
    'ggt':'$section.laboratory.data.ggt', # no preferred units
    'chloride':'$section.laboratory.data.chloride', # no preferredu nits
    'totalBilirubin': '$section.laboratory.data.totalBilirubin', # no preferred units
    'directBilirubin':'$section.laboratory.data.directBilirubin', # Cannot find in screenrecord # No preferred units
    'indirectBilirubin':'$section.laboratory.data.indirectBilirubin', # Cannot find in screenrecord # No preferred units
    'urea':'$section.laboratory.data.urea',
    'bicarbonate':'$section.laboratory.data.bicarbonate', # Cannot find in screenrecord # No preferred units
    'albumin': '$section.laboratory.data.albumin',
    'sgptAlt': '$section.laboratory.data.sgptAlt', # no preferred units
    'sgotAst': '$section.laboratory.data.sgotAst', # no preferred units
    'sodium':'$section.laboratory.data.sodium', # No preferred units
    'totalProtein':'$section.laboratory.data.totalProtein', # No preferred units
    'globulin':'$section.laboratory.data.globulin', # No preferred units
    'potassium':'$section.laboratory.data.potassium', # No preferred units
    'hba1c':'$section.laboratory.data.hba1c',
    'egfr':'$section.laboratory.data.egfr', # Cannot find in screenrecord
    'albuminuria':'$section.laboratory.data.albuminuria', # NA, need to check if there is .value and .unit
    'family-diabetes':'$section.healthhistory.data.family-diabetes',
    'family-asthmaCOPD':'$section.healthhistory.data.family-asthmaCOPD',
    'family-cancer':'$section.healthhistory.data.family-cancer',
    'family-depression':'$section.healthhistory.data.family-depression',
    'family-heartDisease':'$section.healthhistory.data.family-heartDisease',
    'family-glaucoma':'$section.healthhistory.data.family-glaucoma',
    'family-highCholesterol':'$section.healthhistory.data.family-highCholesterol',
    'family-stroke':'$section.healthhistory.data.family-stroke',
    'family-kidneyFamily':'$section.healthhistory.data.kidneyFamily', # Cannot find in screenrecord
    'family-parentalHypertension':'$section.healthhistory.data.parentalHypertension', # Cannot find in screenrecord
    'habits-alcoholIntake':'$section.healthhistory.data.habits-alcoholIntake',
    'habits-exerciseInAWeek':'$section.healthhistory.data.habits-exerciseInAWeek',
    'habits-smoking':'$section.healthhistory.data.habits-smoking',
    'habits-smokingCategory':'$section.healthhistory.data.habits-smokingCategory',
    'habits-cigarettesSmokingCategory':'$section.healthhistory.data.habits-cigarettesSmokingCategory', # Cannot find in screenrecord
    'medicalHistory-chronicKidneyDisease':'$section.healthhistory.data.medicalHistory-chronicKidneyDisease',
    'medicalHistory-chronicObstructiveDisease':'$section.healthhistory.data.medicalHistory-chronicObstructiveDisease',
    'medicalHistory-depression':'$section.healthhistory.data.medicalHistory-depression',
    'medicalHistory-diabetes':'$section.healthhistory.data.medicalHistory-diabetes',
    'medicalHistory-heartAttack':'$section.healthhistory.data.medicalHistory-heartAttack',
    'medicalHistory-thyroidProblem':'$section.healthhistory.data.medicalHistory-thyroidProblem', # Cannot find in screenrecord
    'medicalHistory-highCholesterol':'$section.healthhistory.data.medicalHistory-highCholesterol', # Cannot find in screenrecord
    'medicalHistory-hypertension':'$section.healthhistory.data.medicalHistory-hypertension',
    'medicalHistory-hypertensionTreatment':'$section.healthhistory.data.medicalHistory-hypertensionTreatment', # Cannot find in screenrecord
    'medicalHistory-kidneyStone':'$section.healthhistory.data.medicalHistory-kidneyStone',
    'medicalHistory-learningDisabilities':'$section.healthhistory.data.medicalHistory-learningDisabilities',
    'medicalHistory-lupus':'$section.healthhistory.data.medicalHistory-lupus', # Cannot find in screenrecord. medicalHistory-systemicLupusErythematosus?
    'medicalHistory-otherChronicConditions':'$section.healthhistory.data.medicalHistory-otherChronicConditions',
    'medicalHistory-peripheralVascularDisease':'$section.healthhistory.data.medicalHistory-peripheralVascularDisease', # Cannot find in screenrecord
    'medicalHistory-rheumatoidArthritis':'$section.healthhistory.data.medicalHistory-rheumatoidArthritis',
    'medicalHistory-stroke':'$section.healthhistory.data.medicalHistory-stroke',
    'medications-antipsychotics':'$section.healthhistory.data.medications-antipsychotics',
    'medications-nsaids':'$section.healthhistory.data.medications-nSAIDs',
    'medications-statins':'$section.healthhistory.data.medications-statins',
    'medications-steroids':'$section.healthhistory.data.medications-steroids',
    'medicalHistory-gestationalDiabetes':'$section.healthhistory.data.medicalHistory-gestationalDiabetes',
    'medicalHistory-polycysticOvarianSyndrome':'$section.healthhistory.data.medicalHistory-polycysticOvarianSyndrome',
}

def retrieve_patient_from_batch(batchid):
    db = connect()

    query = { 'batchid': { '$in': batchid }}
    columns = { '_id': 1}

    screen_record_id = retrieve_document(db, 'batchdata', query, columns)
    return screen_record_id

test = retrieve_patient_from_batch([ObjectId('62d64e299dfed154fb4d9cbc'), ObjectId('62d64e309dfed154fb4d9cbd')])
batchid = [ObjectId('62d64e299dfed154fb4d9cbc'), ObjectId('62d64e309dfed154fb4d9cbd')]

indicators = [key for key in screen_record_projection.keys()]
string_types = set(["Y/N", "Frequency", "Ethinicity", "+ve/-ve", "Neither/One/Both"])

def get_preferred_units(key, company = None, organization = None, gender = None, type = "unit"):
    # Checking order company --> organization --> then gender.

    # Company factors-table
    f = open("data/factors-table.json")
    factors_table = json.load(f)

    temp_altunit = None

    if key in factors_table.keys():
        if "unit" in factors_table[key].keys():
            if type == "unit":
                return factors_table[key]["unit"]
            else:
                temp_altunit = factors_table[key]["unit"]

        if type == "altunit":
            if "altunit" in factors_table[key].keys() and factors_table[key]["altunit"] != "":
                return factors_table[key]["altunit"]
    
    if not (company and organization):
        print('Company or Organization not provided. Unable to check next layer of factor-table')
        return None

    try:
        f = open(f"./mysite/main/data/{organization}_factors/factors-table-{company}.json")
    except:
        print("Invalid Company / Organization")
        return None
    factors_table = json.load(f)

    if key in factors_table.keys():
        if "unit" in factors_table[key].keys():
            if type == "unit":
                return factors_table[key]["unit"]
            else:
                if temp_altunit == None:
                    temp_altunit = factors_table[key]["unit"]
        
        if type == "altunit":
            if "altunit" in factors_table[key].keys() and factors_table[key]["altunit"] != "":
                return factors_table[key]["altunit"]
    
    if not gender:
        print('Gender not provided. Unable to check next layer of factor-table')
        return None

    try:
        f = open(f"data/{organization}_factors/factors-table-{gender}-{company}.json")
    except:
        print("Invalid Gender")
        return None

    factors_table = json.load(f)

    if key in factors_table.keys():
        if "unit" in factors_table[key].keys():
            if type == "unit":
                return factors_table[key]["unit"]
            else:
                if temp_altunit == None:
                    temp_altunit = factors_table[key]["unit"]
        
        if type == "altunit":
            if "altunit" in factors_table[key].keys() and factors_table[key]["altunit"] != "":
                return factors_table[key]["altunit"]

    if type == "altunit" and temp_altunit != None:
        return temp_altunit
    
    return None

def export_base_csv(batchid, company, organization):
    error = False
    db = connect()

    screen_record_id = retrieve_patient_from_batch(batchid)
    ids = [ str(x['_id']) for x in screen_record_id ]

    db_col = db["screenrecord"]
    # have to use aggregate here.

    pipeline = [
        {
            "$match": { 
                "batch_report.id": { "$in": ids }
            }
        },

        {
            "$project": screen_record_projection
        }
    ]

    docs = db_col.aggregate(pipeline)

    records = []

    # Track which indicators has no units in factors-table
    indicators_no_units = set()
    
    # iterate through each record retrieved from db
    for index, record in enumerate(docs):
        print(index, record)

        temp_patient = {}
        remarks = ""

        for key in indicators:
            if key in record:
                preferred_units = get_preferred_units(key, company, organization, record.get("gender"), type = "unit")
                value = record[key]
                if type(value) == dict:
                    
                    if preferred_units == None:
                        # No possible units from factors table.
                        indicators_no_units.add(key)

                        if value["unit"] in string_types:
                            try:
                                temp_patient[key] = str(value["value"])
                            except:
                                temp_patient[key] = value["value"]
                                remarks = remarks + ", " + key + " - Invalid Data Type"
                        
                        else:
                            try:
                                temp_patient[key] = float(value["value"])
                            except:
                                temp_patient[key] = value["value"]
                                remarks = remarks + ", " + key + " - Invalid Data Type"

                    else:
                        if value["unit"] in string_types:
                            if value["unit"] != preferred_units:
                                try:
                                    temp_patient[key] = str(value["value"])
                                    remarks = remarks + ", " + key + " - Units not as specified in factors-table"
                                except:
                                    temp_patient[key] = value["value"]
                                    remarks = remarks + ", " + key + " - Invalid Data Type & Units not as specified in factors-table"
                            else:
                                try:
                                    temp_patient[key] = str(value["value"])
                                except:
                                    temp_patient[key] = value["value"]
                                    remarks = remarks + ", " + key + " - Invalid Data Type"
                        else:
                            if value["unit"] != preferred_units:
                                try:
                                    new_value = unit_convertor(key, float(value["value"]), value["unit"], preferred_units)
                                    temp_patient[key] = new_value
                                except:
                                    temp_patient[key] = value["value"]
                                    remarks = remarks + ", " + key + " - Invalid Data Type"
                            else:
                                try:
                                    temp_patient[key] = float(value["value"])
                                except:
                                    temp_patient[key] = value["value"]

                # Unit not specified in DB
                else:
                    # Unvalidated data.
                    if preferred_units == None:
                        indicators_no_units.add(key)
                        # try to convert to string
                        try:
                            temp_patient[key] = float(value)
                        except:
                            temp_patient[key] = value
                    else:
                        if preferred_units in string_types:
                            try:
                                temp_patient[key] = str(value)
                            except:
                                temp_patient[key] = value
                                remarks = remarks + ", " + key + " - Invalid Data Type"
                        
                        else:
                            try:
                                temp_patient[key] = float(value)
                                remarks = remarks + ", " + key + " - Initial Units not specfied"
                            except:
                                temp_patient[key] = value
                                remarks = remarks + ", " + key + " - Invalid Data Type & Initial Units not specfied"
                        
            # Does not exist
            else:
                temp_patient[key] = ""
                remarks = remarks + ", " + key + " - Data missing"
   

        temp_patient["Remarks"] = remarks
        if remarks != "":
            error = True
        records.append(temp_patient)

    # compare to config file for preferred units. if not available just store it as another dictionary.
    patient_records_df = pd.DataFrame.from_records(records)
    # mk temp dir
    folder_name = "temp"
    os.makedirs(f"././{folder_name}")

    # save into temp file
    patient_records_df.to_csv(f"./{folder_name}/validated_data_with_base_units.csv")

    return patient_records_df, indicators_no_units, error


result_df, indicators_no_units = export_base_csv(batchid, 'Parkway Health', 'meshbio')
