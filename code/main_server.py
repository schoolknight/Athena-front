from flask import Flask, jsonify, request
from flask import render_template
#import configparser
import pymongo
import time
from bson import ObjectId
app = Flask(__name__)


# mongodb connnection

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



@app.route('/get_deals')
def getDeals():
    deal_list = deal_col.find({})
    res = []
    for item in deal_list:
        item['_id'] = str(item['_id'])
        #item['createdAt'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['createdAt']));
        res.append(item)
    return jsonify(res)


@app.route('/dashboard')
def dashBoard():
    return render_template('dashboard.html')

@app.route('/phone/<num>')
def phone(num):
    deal_list = deal_col.find()
    res = []
    for item in deal_list:
        item['_id'] = str(item['_id'])
        #item['createdAt'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['createdAt']));
        res.append(item)
    if int(num) > 0 and len(res) > int(num):
        return render_template('phone.html',deal_list=res, if_toast=1)
    else:
        return render_template('phone.html',deal_list=res, if_toast=0) 

@app.route('/hospital/<num>')
def hospital(num):
    deal_list = deal_col.find()
    res = []
    for item in deal_list:
        item['_id'] = str(item['_id'])
        #item['createdAt'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['createdAt']));
        res.append(item)
    if int(num) > 0 and len(res) > int(num):
        return render_template('hospital.html',deal_list=res, if_toast=1)
    else:
        return render_template('hospital.html',deal_list=res, if_toast=0)

@app.route('/patient_operate')
def patientOperate():
    deal_id = request.args.get('deal')
    op_type = int(request.args.get('op')) + 1
    deal_col.update_one({'_id': ObjectId(deal_id)}, {'$set':{'patient_permit': op_type}})
    return 'ok'

@app.route('/hospital_operate')
def hospitalOperate():
    deal_id = request.args.get('deal')
    op_type = int(request.args.get('op')) + 1
    deal_col.update_one({'_id': ObjectId(deal_id)}, {'$set':{'hospital_permit': op_type}})
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

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=25000,debug=True)
