import os
from flask import Flask
from flask import render_template
from flask import json, url_for, jsonify
#import configparser
import pymongo
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
data_rel_path = "data.json"
data_path = os.path.join(server_dir, data_rel_path)
order_path = os.path.join(server_dir, "order.json")
print(order_path)

patient_deal_list = [{'id':0,'t': 0}]

@app.route('/dashboard')
def dashBoard():
    return render_template('dashboard.html')

@app.route('/phone')
def phone():
    return render_template('phone.html',list=patient_deal_list)

@app.route('/patient_agree')
def aptientAgree():
    patient_deal_list.append({'id':len(patient_deal_list), 't':1})
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
    orders = json.load(open(order_path))
    return jsonify(orders)

@app.route('/api/data', methods=['GET'])
def getData():
    data = json.load(open(data_path))
    return jsonify(data)

@app.route('/api/service', methods=['POST'])
def postService():
    print("serviceJSON received!")


# @app.route('/api/balance', methods=['GET'])
# def getBalance():
#     res = []
#     for item in balance:
#         #processing
#         res.append(item)
# return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
