from flask import Flask, render_template, Response, request, redirect, url_for
from firebasetest import get_data, final_result
from flask_cors import CORS
app = Flask(__name__, static_url_path='')
CORS(app)
@app.route("/")
def page2():
    return render_template('page2.html')

@app.route("/forward/", methods=['GET'])
def move_forward():
    #Moving forward code
    # res = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    data = get_data()
    data1 = data[0]
    data2 = data[1]
    CompanyName1 = data[2]
    CompanyName2 = data[3]
    return render_template('page2.html', data1=data1, data2=data2, CompanyName1=CompanyName1, CompanyName2=CompanyName2)

if __name__ == '__main__':
    app.run(host='localhost', port=3000)

