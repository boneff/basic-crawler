import pymongo
# TODO - add config


def init_client(connection_string):
    return pymongo.MongoClient(connection_string)


def get_collection_from_database(client, db_name, collection_name):
    mydb = client[db_name]
    return mydb[collection_name]


mydict = {"name": "John", "address": "Highway 37"}

x = mycol.insert_one(mydict)

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
    print("The database exists.")

collist = mydb.list_collection_names()
if "customers" in collist:
    print("The collection exists.")