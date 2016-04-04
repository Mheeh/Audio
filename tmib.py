from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def audio():
    return render_template('audio.html')


if __name__ == '__main__':
    app.run()
