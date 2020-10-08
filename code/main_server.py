import os
from flask import Flask, jsonify, request
from flask import render_template
from flask import json
from datetime import datetime
import pymongo
import time
from bson import ObjectId

app = Flask(__name__)

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

server_dir = os.path.dirname(__file__)
data_path = os.path.join(server_dir, "data.json")
order_path = os.path.join(server_dir, "order.json")
balance_path = os.path.join(server_dir, "balance.json")

service_id = 13321
HOSPITAL = ['BH1', 'BH2', 'BH3']
DEPARTMENT = ['Internal Medicine', 'Surgery']
DISEASE = ['Diabetes', 'Heart Disease']
GENDER = ['Male' 'Female']
AGE_RANGE = ['<20', '20-30', '30-40', '40-50', '50-60', '60-70', '>70']
FUNCTION=['Distribution', 'SUM', 'Median', 'Linear Regression', 'SVM', 'Linear Model 1']


@app.route('/get_deals')
def getDeals():
    deal_list = deal_col.find({'status':0})
    res = []
    for item in deal_list:
        item['_id'] = str(item['_id'])
        item['createdAt'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['createdAt']));
        res.append(item)
    return jsonify(res)


@app.route('/dashboard')
def dashBoard():
    return render_template('dashboard.html')

@app.route('/phone/<tar_id>')
def phone(tar_id):
    deal_list = deal_col.find()
    res = []
    for item in deal_list:
        item['_id'] = str(item['_id'])
        item['createdAt'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['createdAt']));
        res.append(item)
    return render_template('phone.html',deal_list=res, patient_id=int(tar_id))

@app.route('/patient_operate')
def patientOpeerate():
    deal_id = request.args.get('deal')
    patient_id = int(request.args.get('patient'))
    op_type = int(request.args.get('op')) + 1

    update_item = {}
    update_item['patient.'+ str(patient_id)] = op_type
    print(update_item)
    deal_col.update_one({'_id': ObjectId(deal_id)}, {'$set':update_item})
    return 'ok'

@app.route('/athena')
def athena():
    return render_template('athena.html')

@app.route('/athena-service')
def athena_service():
    return render_template('athena-service.html')

@app.route('/athena-order')
def athena_order():
        return render_template('athena-order.html')

@app.route('/athena-statistics')
def athena_statistics():
        return render_template('athena-statistics.html')

@app.route('/athena-balance')
def athena_balance():
        return render_template('athena-balance.html')

@app.route('/athena-login')
def athena_login():
        return render_template('athena-login.html')

@app.route('/athena-test')
def athena_test():
        return render_template('v-4.html')

@app.route('/api/order', methods=['GET'])
def getOrders():
    deal_list = deal_col.find()
    res = []
    for item in deal_list:
        res_item = {}
        res_item['service_id'] = str(item['service_id'])
        res_item['issue_time'] = item['issue_time']
        res_item['hospitals'] = [str(hos) for hos in item['hospitals']]
        res_item['record_num'] = str(item['record_num'])
        res_item['order_status'] = item['order_status']
        res_item['exec_status'] = item['exec_status']
        res_item['function'] = FUNCTION[item['function']]
        res_item['fixed_fee'] = str(item['fixed_fee'])
        res_item['security'] = item['security']
        res.append(res_item)

    return jsonify(res)


@app.route('/api/balance', methods=['GET'])
def getBalance():
    deal_list = deal_col.find({'balance_done': 1})
    res = []
    for item in deal_list:
        res_item = {}
        res_item['service_id'] = str(item['service_id'])
        res_item['issue_time'] = item['issue_time']
        res_item['hospitals'] = [str(hos) for hos in item['hospitals']]
        res_item['hospital_fee'] = [str(rec*0.5) for rec in item['record_num'])
        res_item['func_fee'] = str(item['func_fee'])
        res_item['exec_fee'] = str(int(item['exec_sec'] * 2/3))
        res_item['total_fee'] = str(item['fixed_fee'] + res_item['exec_fee'] + item['func_fee'])

        res.append(res_item)

    return jsonify(res)


@app.route('/api/data', methods=['POST'])
def getData():
    filter = request.get_json()

    #add query builder
    data_query = {'$and':[{'hospital': {'$in': filter.hospitals},
                    'department': {'$in': filter.department},
                    'disease': {'$in': filter.disease},
                    'gender': {'$in': filter.gender},
                    'age_range': {'$in': filter.age_range}}]}

    data_list = data_col.find(data_query)
    res = []
    for item in data_list:
        res_item = {}
        res_item['hospital'] = HOSPITAL[item['hospital']]
        res_item['department'] = DEPARTMENT[item['department']]
        res_item['disease'] = DISEASE[item['disease']]
        res_item['gender'] = GENDER[item['gender']]
        res_item['age_range'] = AGE_RANGE[item['age_range']]
        res.append(res_item)

    return jsonify(res)

@app.route('/api/service', methods=['POST'])
def postService():
    global service_id
    service = request.get_json()
    dt_string = datetime.now()

    deal = {}
    deal['service_id'] = service_id
    service_id += 1
    deal['issue_time'] = dt_string.strftime("%Y-%m-%d %H:%M:%S")
    deal['exec_status'] = 2
    deal['exec_sec'] = 0
    deal['order_status'] = 1
    deal['hospitals'] = service['hospitals']
    deal['record_num'] = service['record_num']
    deal['func']=service['func']
    deal['fixed_fee']=service['fixed_fee']
    deal['security']=service['security']
    deal['record_total']=service['record_total']
    deal['func_fee']=service['func_fee']
    deal['balance_done'] = 1
    deal['result'] = {}

    print(deal)

    deal_col.insert_one(deal)

    authorization and update exec_status
    deal_col.update_one({'service_id': service_id - 1}, {'$set': {'exec_status':1}})

    switch (service['func']) {
        # Distribution
        case 0:
            result = {}
            break;

        # Linear regression
        case 3:
            result = {}
            break;

            # Linear Model 1
        case 5:
            result = {}
            break;
        default:
            print("unidentified function!\n")
        }

    #execution
    ok, exec_sec = call_func(service['func'])
    if not ok:
        print("calling function failed!\n")
    else:
        print("calling function succeed!\n")
        deal_col.update_one({'service_id': service_id - 1}, {'$set': {'exec_status':0}})
        deal_col.update_one({'service_id': service_id - 1}, {'$set': {'order_status':0}})
        deal_col.update_one({'service_id': service_id - 1}, {'$set': {'balance_done':0}})
        res = {'$set': {'result': result}}
        deal_col.update_one({'service_id': service_id - 1}, res)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


def call_func(id):
    #calling sgx function

    return 0, 30


if __name__ == '__main__':
    # clear deal table
    # count = deal_col.delete_many({})

    # connect with sgx machine
    app.run(debug=True)
