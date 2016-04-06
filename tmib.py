from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/play')
def play():
    return render_template('play.html')


@app.route('/library')
def library():
    library = os.listdir(app.static_folder + '/music')
    library.sort()

    return render_template('library.html', library=library)

if __name__ == '__main__':
    app.run()
