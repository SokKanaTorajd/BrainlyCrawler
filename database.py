from pymongo import MongoClient

class dbBrainly():
    client = MongoClient()
    database = 'brainlydb'

    def insert_url(self, collection, url):
        db  = self.client[self.database]
        db[collection].insert_one({'url':url})

    
