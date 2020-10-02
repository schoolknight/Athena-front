from flask import Flask
from flask import render_template
import configparser
import pymongo
app = Flask(__name__)


# mongodb connnection
conf= configparser.ConfigParser()
conf.read('./server.conf')
uri = conf.get("mongodb", "uri")
database_str = conf.get("mongodb", "database")
data_col_str = conf.get("mongodb", "data_col")
mongo = pymongo.MongoClient(uri)
data_col = mongo[database_str][data_col_str]


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

if __name__ == '__main__':
    app.run(debug=True)
