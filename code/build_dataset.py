from sklearn import datasets
import pymongo
import random
import configparser

diabetes = datasets.load_diabetes()

f = open('server.conf')
lines = f.readlines()
f.close()

uri = lines[0].strip()
database_str = lines[1].strip()
data_col_str = lines[2].strip()
deal_col_str = lines[3].strip()
mongo = pymongo.MongoClient(uri)
data_col = mongo[database_str][data_col_str]
deal_col = mongo[database_str][deal_col_str]

insert_list = []
for item in diabetes.data:
    cur_age = float(item[0])* 420 + 50
    cur_range = int(cur_age / 10) - 2
    if cur_range < 0:
        cur_range = 0
    if cur_range > 6:
        cur_range = 6
    cur_sex = 0
    if float(item[1]) > 0:
        cur_sex = 1

    tmp_item = {
        'hospital': random.randint(0,2),
        'department': 0,
        'disease':0,
        'age_range': cur_range,
        'age':cur_age,
        'sex':cur_sex,
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