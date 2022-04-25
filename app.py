from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from pprint import pprint
import json

import logic.proceed as Proceed
import logic.chords_new as Chords
import logic.config as Config

app = Flask(__name__)

@app.route("/")
def home():
    return "home"

@app.route('/getchords')
def getChordsByBar():
    queries = request.args
    return queries.get("midi")

@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("uploading..")
    if(request.method == 'POST'):
        pprint(request.values)
        f = request.files['midi']
        pprint(f)
        f.save(f"static/uploads/{secure_filename(f.filename)}")
        pprint(f)
    return redirect(url_for('play_app', name=f.filename.replace('.mid', '')))

@app.route('/play')
def play_app():
    playing = request.args.get('name')
    alter_key = Chords.getNumber(request.args.get('alter_key')) if request.args.get('alter_key') else -1
    press_number = request.args.get('press_number') if request.args.get('press_number') else 2


    print(playing)
    result_packs = Proceed.proceed(playing, int(press_number), alter_key)

    return render_template('app.html',packs = result_packs, playing = playing)
