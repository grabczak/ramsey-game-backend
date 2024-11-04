from flask import Flask, request
from flask_cors import CORS

import json
import random

from graph_logic import json_to_networkx, find_best

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

    target_clique_size = data.get('target_clique_size')

    # print(json.dumps(data, indent = 4))

    graph = data.get('graph')

    edges = graph.get('edges')

    data = find_best(edges, target_clique_size)

    # best_edge = data['edge']

    # return best_edge

    return data
