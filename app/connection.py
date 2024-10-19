from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL_DB = os.getenv("MONGO_URL_DB")
CONN_STRING, DB_NAME = "".join(MONGO_URL_DB.split("/")[:-1]), MONGO_URL_DB.split("/")[-1]
COLLECTION_NAME = "samplePaper"

client = MongoClient(CONN_STRING)
db = client[DB_NAME]

def get_collection():
    return db[COLLECTION_NAME]


