from flask import Flask
from flask import render_template
app = Flask(__name__)


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

if __name__ == '__main__':    
    app.run(debug=True)    