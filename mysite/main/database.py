from pymongo import MongoClient

# hide username and password in the future.
mongo_url = "mongodb+srv://capstone:8vUr83VXefLJcyxkJJ55V1z1smQ0N10z@cluster0.succu.mongodb.net/test?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=true"

# database is string of database
def connect(database = "meshbio"):
    client = MongoClient(mongo_url)
    db = client[database]
    return db

# collection is name of collection in string
# db is db connection obtained from connect()
def get_collection(collection, db):
    db_col = None
    try:
        db_col = db[collection]
    except Exception as ex:
        error_msg = f"Error connecting to collection: {ex}"
        # logger.error(error_msg)
        raise Exception(error_msg)
    return db_col

def retrieve_document(db, collection, query, columns={}):
    db_col = get_collection(collection, db)
    if db_col is None:
        return None

    documents = None
    required_columns = {x: 1 for x in columns}
    try:
        documents = db_col.find(query, required_columns)
        documents = [x for x in documents]
    except Exception as ex:
        error_msg = f"Error executing find '{query}' from {collection}: {ex}"
        # logger.error(error_msg)
        raise Exception(error_msg)
    # if documents is not None:
    #     logger.info(f"{len(documents)} documents retrieved from {collection}")

    return documents