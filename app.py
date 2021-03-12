#app.py
# Importieren von notige Flask Elementen - Flask ist eine Server Framework für die Client
from flask import Flask, render_template, request, json, session, url_for
from flask_session import Session
import requests

# für entwicklung ist eine dotenv nötig in operating system
import os
keyinfo = os.getenv("KEY_INFO")

app = Flask(__name__)
#session key
app.secret_key="richard"
# sollte auf server gespeichert (lokalle Festplatte) und für app verfügbar
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)

# Variable Deklaration und Initialisierung
displayed = False
picturedataarray=[]

# Bei anlauf des Program sind diesen Aktion gemacht
# Sie sind eine Dictionary von mögliche Bilder Addressen, 3 mal Geholt
@app.before_first_request
def load_from_API():
    # Was gesucht sein sollen - API schlussel (in .env File), suchen nach donald trump, alle Bild typen und nur 10 Antworten
    parameters = {
        'key': keyinfo,
        'q': 'donald+trump',
        'image_type': 'all',
        'per_page': 10,
    }
    #Abholung von den Bilder Info und Addressen bie pixabay
    responsedon = requests.get('https://pixabay.com/api/', params=parameters)
    respdon=responsedon.json()

    # Gleichen wie oben nür mit Putin und Merkel
    parameters = {
        'key': keyinfo,
        'q': 'putin',
        'image_type': 'all',
        'per_page': 10,
    }
    responseput = requests.get('https://pixabay.com/api/', params=parameters)
    respput = responseput.json()

    parameters = {
        'key': keyinfo,
        'q': 'angela+merkel',
        'image_type': 'all',
        'per_page': 10,
    }
    responseangie = requests.get('https://pixabay.com/api/', params=parameters)
    respangie = responseangie.json()
    #Als session Data gespeichert - Information von Bilder
    session['API_data'] = [respdon['hits'], respput['hits'], respangie['hits']]

# Base route für Server - sendet die möglicher Bilder Addresse auf die Client nür wann es gibt Datei in session
@app.route('/')
def load_up_choice():
    if "API_data" in session:
        return render_template('demo.html', respdon=session["API_data"][0], respput=session["API_data"][1], respangie=session["API_data"][2])
    else:
        return 'Something has gone wrong, please refresh'

#nach die Wahl von eine Bild ist die addresse zu den display template geschicht
#benutzung von 'apply' macht die Text in den Bild und gibt eine Änderung in den Display Variable
@app.route('/display/', methods=['POST', 'GET'])
def displ():
    if request.method=='POST':
        if "submit-img" in request.form:
            myformdata = request.form["submit-img"]
            # Muss die getauscht zwischen " und ' (Python problem?)
            myjsoncompatibility = myformdata.replace("'", '"')
            # In session data gespeichert
            jsoneddata = json.loads(myjsoncompatibility)
            session['picdata']=jsoneddata
            displayed = False
            # Gewählte Bilder Data zu Template geschicht
            return render_template('display.html', jsoneddata=jsoneddata, topText="", bottomText="", textColor="black", textSize="30", displayed=displayed)
        elif "apply" in request.form:
            # Text Data in Bild verbunden
            displayed = True
            return render_template('display.html', jsoneddata=session['picdata'], topText=request.form["topText"], bottomText=request.form["bottomText"], textColor=request.form["textColor"], textSize=request.form["textSize"], displayed=displayed)

# kann mann mit Wiederhollung nür deine ausgewählte Bild sehen
# Läuft wann Try-Again button benutzt
    else:
        displayed = False
        # Text weg von Bild
        return render_template('display.html', jsoneddata=session['picdata'], topText="", bottomText="",
                               textColor="black", textSize="30", displayed=displayed)

# Route 'Saved' Bildern anzuschauen
@app.route('/saved/', methods=['POST', 'GET'])
def saveInterface():
    if request.method=='POST':
        # JSON in normaller Data umwandeln
        pictureJSON = request.form['picturedata']
        picturedata = json.loads(pictureJSON)

        # Korrektur wegen Problem mit Data
        picturedata = picturedata.replace(' ', '+')

        # Kann nur die neuste 10 Bild in die Session zeigen
        lengthOfArray=len(picturedataarray)
        if lengthOfArray > 10:
            del picturedataarray[0]

        # neue Bild zu Array
        picturedataarray.append(picturedata)
        session['allpicturedata'] = json.dumps(picturedataarray)
        return 'Hello'

# Wann von Saved Button in Header
    else:
        # Array von Pic data in Template eingeladen.
        return render_template('allsaved.html', savedMeme=picturedataarray )

if __name__ == '__main__':
    app.run(debug=True)