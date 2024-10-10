from flask import Flask

app = Flask(__name__)

@app.after_request
def request_callback(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
