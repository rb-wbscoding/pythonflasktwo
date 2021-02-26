from flask import Flask, render_template, request, json, session
import requests


#from flask.json import JSONEncoder, JSONDecoder

app = Flask(__name__)
app.secret_key="richard"


@app.before_first_request
def load_from_API():
    parameters = {
        'key': '17706064-dbf47c15f3ffee1df9f90dd47',
        'q': 'donald+trump',
        'image_type': 'all',
        'per_page': 20,
    }
    responsedon = requests.get('https://pixabay.com/api/', params=parameters)
    respdon=responsedon.json()

    parameters = {
        'key': '17706064-dbf47c15f3ffee1df9f90dd47',
        'q': 'putin',
        'image_type': 'all',
        'per_page': 20,
    }
    responseput = requests.get('https://pixabay.com/api/', params=parameters)
    respput = responseput.json()

    parameters = {
        'key': '17706064-dbf47c15f3ffee1df9f90dd47',
        'q': 'angela+merkel',
        'image_type': 'all',
        'per_page': 20,
    }
    responseangie = requests.get('https://pixabay.com/api/', params=parameters)
    respangie = responseangie.json()
    session['API_data'] = [respdon, respput, respangie]


@app.route('/')
def load_up_choice():
    if "API_data" in session:
        alldata = session["API_data"]
        return render_template('demo.html', respdon=alldata[0], respput=alldata[1], respangie=alldata[2])
    else:
        return 'waiting'

@app.route('/display/', methods=['POST', 'GET'])
def displ():
    if request.method == "POST":
        myformdata = request.form["submit-img"]
        myjsoncompatibility = myformdata.replace("'", '"')
        jsoneddata = json.loads(myjsoncompatibility)
        return render_template('display.html', jsoneddata=jsoneddata)



if __name__ == '__main__':
    app.run(debug=True)