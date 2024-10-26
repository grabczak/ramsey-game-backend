from flask import Flask, request
from flask_cors import CORS

import random

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/play', methods=['POST'])
def play():
    content_type = request.headers.get('Content-Type')
    
    if (content_type != 'application/json'):
        return 'Content-Type not supported'

    data = request.json.get('data')

    graph = data.get('graph')

    edges = graph.get('edges')

    available_edges = list(filter(lambda x: x.get('team') == 'none', edges))

    random_edge = random.choice(available_edges)

    return random_edge
