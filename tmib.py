from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/play')
def play():
    return render_template('play.html')


@app.route('/library')
def library():
    return render_template('library.html')

if __name__ == '__main__':
    app.run()
