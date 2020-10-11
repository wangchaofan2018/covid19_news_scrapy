import pymongo
import covid_19.settings as settings
import sys
from flashtext import KeywordProcessor

client = pymongo.MongoClient(settings.MONGO_DB_URI)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]
deleteColl = db["deleteColl"]
mydoc = collection.find()
kw_list = ["新冠","疫情","抗疫","病例"]
keyword_processor = KeywordProcessor()
for keyword in kw_list:
    keyword_processor.add_keyword(keyword)
for item in mydoc:
    find_title = keyword_processor.extract_keyword(item["title"])
    find_content = keyword_processor.extract_keyword(item["content"])
    if not (find_title or find_content):
        deleteColl.insert_one(item)
        myDeleteQuery = {"_id",item["_id"]}
        collection.delete_one(myDeleteQuery)
    