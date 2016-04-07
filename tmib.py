from flask import Flask, redirect, render_template, request, url_for
from werkzeug import utils
import os

app = Flask(__name__)

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
    if request.method == 'POST':
        file = request.files['music']
        if file and allowed_file(file.filename):
            filename = utils.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('library'))

    library = os.listdir(app.config['UPLOAD_FOLDER'])
    library.sort()

    return render_template('library.html', library=library)

if __name__ == '__main__':
    app.run()
