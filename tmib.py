#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import flash, Flask, Markup, redirect, render_template, request, url_for
from werkzeug import utils
import os

app = Flask(__name__)
app.secret_key = 'tmib@put'

UPLOAD_FOLDER = app.static_folder + '/music'
ALLOWED_EXTENSIONS = set(['wav'])
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
            if filename in library:
                flash(Markup(u'Utwór o nazwie <font style="font-style: italic">' + unicode(filename) + u'</font> już istnieje. Zmień nazwę pliku i spróbuj ponownie.'), 'danger')
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash(Markup(u'Utwór dodano jako <font style="font-style: italic">' + unicode(filename) + u'</font>.'), 'success')

        return redirect(url_for('library'))

    return render_template('library.html', library=library)

if __name__ == '__main__':
    app.run()
