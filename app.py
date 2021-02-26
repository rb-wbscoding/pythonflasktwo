from flask import Flask, render_template, request, json
import requests
#from flask.json import JSONEncoder, JSONDecoder

app = Flask(__name__)


@app.route('/')
def hello_world():
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

    return render_template('demo.html', respdon=respdon, respput=respput, respangie=respangie)

@app.route('/display/', methods=['POST', 'GET'])
def displ():
    if request.method == "POST":
        myformdata = request.form["submit-img"]
        myjsoncompatibility = myformdata.replace("'", '"')
        jsoneddata = json.loads(myjsoncompatibility)
        return render_template('display.html', jsoneddata=jsoneddata)



if __name__ == '__main__':
    app.run(debug=True)