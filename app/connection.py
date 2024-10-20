from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

CONN_STRING = os.getenv("CONN_STRING")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = "samplePaper"
TASK_COLLECTION_NAME = "tasks"

client = MongoClient(CONN_STRING)
db = client[DB_NAME]

def get_collection():
    return db[COLLECTION_NAME]

def get_task_collection():
    return db[TASK_COLLECTION_NAME]


