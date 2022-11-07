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
def generate_corp_report(report_data, _reportid = 0):

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
    if _reportid == 0:
        audit_dic['reportid'] = inserted_doc.inserted_id
        update_audit_trail(audit_dic)
        return report_data["created_by"]["name"], report_data["last_generated_time"], inserted_doc.inserted_id
    else:
        audit_dic['reportid'] = _reportid
        update_audit_trail(audit_dic)
        return report_data["created_by"]["name"], report_data["last_generated_time"], _reportid

    

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
    # print('retrieve audit trail')
    # print(reportid)
    # print(type(reportid))
    # print(reportid)
    audit_trails = retrieve_document(db, 'audittrail',{'reportid':reportid})
    return audit_trails
    
def retrieve_corporate_report_data(organization):

    temp_url = "mongodb://localhost:27017"
    client = MongoClient(temp_url)
    db = client["meshbio"]

    query = {'organization': organization}
    columns = { 'name': 1, 'batches': 1, 'last_generated_time': 1, 'status': 1 }

    report_data = retrieve_document(db, 'corporatereportdata', query, columns)

    for report in report_data:
        batches = report['batches']
        batch_names = []
        for batch in batches:
            query1 = { '_id': ObjectId(batch)}
            columns1 = { 'name': 1 }
            batch_name = retrieve_document(db, 'corporatebatch', query1, columns1)
            print(batch_name)
            batch_names.append(batch_name[0]['name'])
        report['batches'] = batch_names


    return report_data
