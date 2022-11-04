from .database import *
from pymongo import MongoClient
#ObjectId
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from datetime import datetime
import json
def get_corporate_list(organization):

    '''
    #db = connect()
    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]

    query = { 'organization': organization }
    columns = { 'name': 1}
    corporates = retrieve_document(db, 'corporatelist', query, columns)
    '''

    file_path = "/home/joel/demo/data/corporatelist.json"

    with open(file_path, "r") as fp:
        data = json.load(fp)
        
    corporates = [item for item in data if item["organization"] == organization]
    corporates = [{"name": item["name"], "_id": item["_id"]} for item in corporates]
    return corporates


def get_batchid_list(organization, corporate):

    temp_url = 'mongodb://capstone:P5O22WPAKzDQF45v@13.212.225.13:27017/meshbio?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(temp_url)
    db = client["meshbio"]
    #db = connect()
    query = { 'organization': organization, 'Company': corporate }
    columns = { 'batchid': 1 }
    batchid = retrieve_document(db, 'batchdata', query, columns)
    return batchid

# organization is String name, corporate is ObjectId.
def get_batch_list(organization, corporate):
    '''
    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]

    query = { 'organization': organization, 'corporateid': ObjectId(corporate) }
    columns = { 'name': 1 }
    batchlist = retrieve_document(db, 'corporatebatch', query, columns)

    return batchlist
    '''
    file_path = "/home/joel/demo/data/corporatebatch.json"
    with open(file_path, "r") as fp:
        data = json.load(fp)
    
    batchlist = [item for item in data if item["organization"] == organization and item["corporateid"] == corporate]
    batchlist = [{"name": item["name"], "_id": item["_id"]} for item in batchlist]

    return batchlist


def get_report(organization, corporate, batchid):
    
    temp_url = 'mongodb://capstone:P5O22WPAKzDQF45v@13.212.225.13:27017/meshbio?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(temp_url)
    db = client["meshbio"]

    #db = connect()
    query = {'organization': organization, 'Company': corporate, 'batchid': batchid }
    columns = {'report': 1}
    reports = retrieve_document(db, 'batchdata', query, columns)
    return reports

# report data is a dictionary. keys = [organization, corporateid, name, batches (array of batchid), report_template, report_type, created_by (dictionary)]
def generate_corp_report(report_data):

    # temp_url = "mongodb://localhost:27017"
    # client = MongoClient(temp_url)
    # db = client["meshbio"]
    # collection = db["corporatereportdata"]

    file_path = "/home/joel/demo/data/corporatereportdata.json"
    with open(file_path, "r") as fp:
        data = json.load(fp)

    report_data["status"] = "Ready" # Hardcoded for now
    report_data["last_generated_time"] = datetime.now()

    # inserted_doc = collection.insert_one(report_data)
    doc_id = {"$oid": str(ObjectId())}
    report_data["_id"] = doc_id

    report_data["batches"] = [str(x) for x in report_data["batches"]]
    report_data["created_by"]["created_time"] =  report_data["created_by"]["created_time"].strftime("%y-%m-%d")
    report_data["last_generated_time"] =  report_data["last_generated_time"].strftime("%y-%m-%d")

    data.append(report_data)
    with open(file_path, "w", encoding='utf-8') as ufp:
        json.dump(data, ufp, ensure_ascii=False, indent=4)

    audit_dic = {}

    audit_dic['datetime'] = datetime.now().strftime("%y-%m-%d")
    audit_dic['action'] = 'Report Generated'
    audit_dic['user'] = report_data["created_by"]["name"]
    # audit_dic['reportid'] = inserted_doc.inserted_id
    audit_dic["reportid"] = doc_id

    update_audit_trail(audit_dic)

    # return report_data["created_by"]["name"], report_data["last_generated_time"], inserted_doc.inserted_id
    return report_data["created_by"]["name"], report_data["last_generated_time"], doc_id

# audit_dic - keys (datetime, action, user, report_id)
def update_audit_trail(audit_dic):
    # temp_url = "mongodb://localhost:27017"
    # client = MongoClient(temp_url)
    # db = client["meshbio"]
    # collection = db["audittrail"]

    # inserted_doc  = collection.insert_one(audit_dic)
    file_path = "/home/joel/demo/data/audittrail.json"
    with open(file_path, "r") as fp:
        data = json.load(fp)
    print("A")
    print(data)
    data.append(audit_dic)
    print("B")
    print(data)

    with open(file_path, "w", encoding='utf-8') as ufp:
        json.dump(data, ufp, ensure_ascii=False, indent=4)


def retrieve_audit_trail(reportid):
    # temp_url = "mongodb://localhost:27017"
    # client = MongoClient(temp_url)
    # db = client["meshbio"]
    print('retrieve audit trail')
    print(reportid)
    print(type(reportid))
    print(reportid)
    # audit_trails = retrieve_document(db, 'audittrail',{'reportid':reportid})

    file_path = "/home/joel/demo/data/audittrail.json"
    with open(file_path, "r") as fp:
        data = json.load(fp)
    
    audit_trails = [item for item in data if item["reportid"] == reportid]
    return audit_trails
    
