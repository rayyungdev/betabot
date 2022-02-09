import collections
from multiprocessing import connection
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
CONNECTION_URL = os.getenv('CONNECTION_URL')

def create_connection(path,db):
    connection = None
    try:
        connection = MongoClient(path)
    except Exception as e:
        print(f"An error occured: \n {e}")
    return connection[db]

def collection_connect(db, collect):
    try:
        collection = db[collect]
        return collection
    except Exception as e:
        print(f'error here {e}')
        
if __name__=="__main__":
    db = create_connection(CONNECTION_URL,"welcomeinfo")
    collection = collection_connect(db, "checkdat")
