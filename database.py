import pymongo
class Database:
    DB=None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        Database.db=client.mydb

    @staticmethod
    def insert_record(doc):
        Database.db.user.insert_one(doc)

    @staticmethod
    def update_record(arg,doc):
        Database.db.user.update(arg,doc)

    @staticmethod
    def delete_record(doc):
        Database.db.user.delete_one(doc)

    @staticmethod
    def get_records():
        records=[doc for doc in Database.db.user.find()]
        return records

    @staticmethod
    def find_record(doc):
        Database.db.user.find(doc)
