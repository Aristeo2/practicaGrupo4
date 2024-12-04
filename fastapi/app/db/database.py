# app/db/database.py
from pymongo import MongoClient
from pymongo.collection import Collection

class Database:
    def __init__(self, db_name: str = "mi_base_de_datos"):
        self.client = MongoClient("mongodb+srv://aristeolg:clinicaVetGr4@cluster0.uylyg.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]
