from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/hello-world')
def index():
    return 'hello, world, 3!'
