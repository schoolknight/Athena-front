from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/dashboard')
def dashBoard():
    return render_template('dashboard.html')

if __name__ == '__main__':    
    app.run(debug=True)    