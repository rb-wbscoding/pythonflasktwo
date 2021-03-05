from flask import Flask, render_template, request, json, session, url_for
from flask_session import Session
import requests
from dotenv import load_dotenv
load_dotenv()
import os
token = os.environ.get("KEY_INFO")

app = Flask(__name__)
app.secret_key="richard"
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)

displayed = False
picturedataarray=[]

@app.before_first_request
def load_from_API():
    parameters = {
        'key': token,
        'q': 'donald+trump',
        'image_type': 'all',
        'per_page': 10,
    }
    responsedon = requests.get('https://pixabay.com/api/', params=parameters)
    respdon=responsedon.json()

    parameters = {
        'key': token,
        'q': 'putin',
        'image_type': 'all',
        'per_page': 10,
    }
    responseput = requests.get('https://pixabay.com/api/', params=parameters)
    respput = responseput.json()

    parameters = {
        'key': token,
        'q': 'angela+merkel',
        'image_type': 'all',
        'per_page': 10,
    }
    responseangie = requests.get('https://pixabay.com/api/', params=parameters)
    respangie = responseangie.json()
    session['API_data'] = [respdon['hits'], respput['hits'], respangie['hits']]

@app.route('/')
def load_up_choice():
    if "API_data" in session:
        return render_template('demo.html', respdon=session["API_data"][0], respput=session["API_data"][1], respangie=session["API_data"][2])
    else:
        return 'Something has gone wrong, please refresh'

@app.route('/display/', methods=['POST', 'GET'])
def displ():
    if request.method=='POST':
        if "submit-img" in request.form:
            myformdata = request.form["submit-img"]
            myjsoncompatibility = myformdata.replace("'", '"')
            jsoneddata = json.loads(myjsoncompatibility)
            session['picdata']=jsoneddata
            displayed = False
            return render_template('display.html', jsoneddata=jsoneddata, topText="", bottomText="", textColor="black", textSize="30", displayed=displayed)
        elif "apply" in request.form:
            displayed = True
            return render_template('display.html', jsoneddata=session['picdata'], topText=request.form["topText"], bottomText=request.form["bottomText"], textColor=request.form["textColor"], textSize=request.form["textSize"], displayed=displayed)
        elif "saved-img" in request.form:
            pictureURL = request.form["saved-img"]
            displayed = False
            return render_template('display.html', jsoneddata= pictureURL, topText="", bottomText="", textColor="black",
                                   textSize="30", displayed=displayed)
    else:
        displayed = False
        return render_template('display.html', jsoneddata=session['picdata'], topText="", bottomText="",
                               textColor="black", textSize="30", displayed=displayed)

@app.route('/saved/', methods=['POST', 'GET'])
def saveInterface():
    if request.method=='POST':
        pictureJSON = request.form['picturedata']
        picturedata = json.loads(pictureJSON)
        picturedata = picturedata.replace(' ', '+')
        lengthOfArray=len(picturedataarray)
        if lengthOfArray > 10:
            del picturedataarray[0]
        picturedataarray.append(picturedata)
        session['allpicturedata'] = json.dumps(picturedataarray)
        return 'Hello'
    else:
        return render_template('allsaved.html', savedMeme=picturedataarray )

if __name__ == '__main__':
    app.run(debug=True)