from .database import *
from pymongo import MongoClient
#ObjectId
from bson.objectid import ObjectId
from datetime import datetime
def get_corporate_list(organization):

    #db = connect()
    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]

    query = { 'organization': organization }
    columns = { 'name': 1}
    corporates = retrieve_document(db, 'corporatelist', query, columns)

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
    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]

    query = { 'organization': organization, 'corporateid': ObjectId(corporate) }
    columns = { 'name': 1 }
    batchlist = retrieve_document(db, 'corporatebatch', query, columns)

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

    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]
    collection = db["corporatereportdata"]

    report_data["status"] = "Ready" # Hardcoded for now
    report_data["last_generated_time"] = datetime.now()

    inserted_doc = collection.insert_one(report_data)

    audit_dic = {}

    audit_dic['datetime'] = datetime.now()
    audit_dic['action'] = 'Report Generated'
    audit_dic['user'] = report_data["created_by"]["name"]
    audit_dic['reportid'] = inserted_doc.inserted_id

    update_audit_trail(audit_dic)

    return report_data["created_by"]["name"], report_data["last_generated_time"], inserted_doc.inserted_id

# audit_dic - keys (datetime, action, user, report_id)
def update_audit_trail(audit_dic):
    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]
    collection = db["audittrail"]

    inserted_doc  = collection.insert_one(audit_dic)


def retrieve_audit_trail(reportid):
    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]
    print('retrieve audit trail')
    print(reportid)
    print(type(reportid))
    print(reportid)
    audit_trails = retrieve_document(db, 'audittrail',{'reportid':reportid})
    return audit_trails
    
