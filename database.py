from pymongo import MongoClient

class dbBrainly():
    client = MongoClient()
    database = 'brainlydb'

    def insert_url(self, collection, url):
        db  = self.client[self.database]
        db[collection].insert_one({'url':url})

    def get_all_urls(self, collection):
        db = self.client[self.database]
        collection = db['bindo']
        result = collection.find()
        return result

    def insert_info(self, collection, data):
        db = self.client[self.database]
        db[collection].insert_one(data)
    
