
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

if __name__ == '__main__':
    app.run(debug=True)
