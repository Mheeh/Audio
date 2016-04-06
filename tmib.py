from flask import Flask, redirect, render_template, url_for
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/play')
@app.route('/play/<music>')
def play(music=None):
    return render_template('play.html', music=music)


@app.route('/library')
def library():
    library = os.listdir(app.static_folder + '/music')
    library.sort()

    return render_template('library.html', library=library)

if __name__ == '__main__':
    app.run()
