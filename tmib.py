#!/usr/bin/python
# -*- coding: utf-8 -*-

# Using: Python 2.7 Anaconda 4.0.0

from flask import flash, Flask, Markup, redirect, render_template, request, url_for
from werkzeug import utils
import amplitude
import os
# TODO CHANGE NAME
import specto

app = Flask(__name__)
app.secret_key = 'tmib@put'

IMAGE_FOLDER = app.static_folder + '/img'
UPLOAD_FOLDER = app.static_folder + '/music'
ALLOWED_EXTENSIONS = set(['wav'])
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/play', methods=['GET'])
@app.route('/play/<music>', methods=['GET'])
def play(music=None):
    return render_template('play.html', music=music)


@app.route('/library', methods=['GET', 'POST'])
def library():
    library = os.listdir(app.config['UPLOAD_FOLDER'])
    library.sort()

    if request.method == 'POST':
        file = request.files['music']
        if file and allowed_file(file.filename):
            filename = utils.secure_filename(file.filename)
            # CZY PLIK ISTNIEJE W BIBLIOTECE?
            # if filename in library:
            #     flash(Markup(u'Utwór o nazwie <font style="font-style: italic">' + unicode(filename) + u'</font> już istnieje. Zmień nazwę pliku i spróbuj ponownie.'), 'danger')
            # else:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # GENEROWANIE OBRAZKÓW
            name = filename.rsplit('.', 1)[0]
            amplitude_name = "a_" + name + ".png"
            spectrogram_name = "s_" + name + ".png"
            amplitude_path = app.config['IMAGE_FOLDER'] + '/amplitudes/' + amplitude_name
            spectrogram_path = app.config['IMAGE_FOLDER'] + '/spectrograms/' + spectrogram_name

            #TODO GENERATE AMPLITUDE AND SPECTROGRAM
            amplitude.plotGraph(file_path, graphpath=amplitude_path)
            specto.plotstft(file_path, plotpath=spectrogram_path)

            flash(Markup(u'Utwór dodano jako <font style="font-style: italic">' + unicode(filename) + u'</font>.'), 'success')
        else:
            flash(u'Plik posiada niedozwolone rozszerzenie.', 'danger')

        return redirect(url_for('library'))

    return render_template('library.html', library=library)

if __name__ == '__main__':
    app.run()
