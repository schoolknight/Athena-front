from sklearn import datasets
import pymongo
import random
import configparser

diabetes = datasets.load_diabetes()

conf= configparser.ConfigParser()
conf.read('./server.ini')
uri = conf.get("mongodb", "uri")
database_str = conf.get("mongodb", "database")
data_col_str = conf.get("mongodb", "data_col")
mongo = pymongo.MongoClient(uri)
data_col = mongo[database_str][data_col_str]

insert_list = []
for item in diabetes.data:
    tmp_item = {
        'hospital': random.randint(0,2),
        'department': 0,
        'age':item[0],
        'sex':item[1],
        'bmi':item[2],
        'bp':item[3],
        's1':item[4],
        's2':item[5],
        's3':item[6],
        's4':item[7],
        's5':item[8],
        's6':item[9] 
    }
    insert_list.append(tmp_item)

res = data_col.insert_many(insert_list)
print(res)