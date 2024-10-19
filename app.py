from flask import Flask, request
from flask_cors import CORS

import random
import networkx as nx

def connect(Graph):
    # --------------------------------------------
    # funkcja bieże graf i zwraca listę wierzchołków
    # sąsiędnich do wierzchołka i 
    #
    # in:
    # Graph - Graf
    #
    # out:
    # connections - wyżej wspomniana lista
    # --------------------------------------------
    connections = []
    nodes = list(Graph.nodes)
    edges = list(Graph.edges)
    for i in range(len(nodes)):
        connections.append([nodes[i]])
        for j in range(len(edges)):
            if edges[j][0] == nodes[i]:
                connections[i].append(edges[j][1])
            if edges[j][1] == nodes[i]:
                connections[i].append(edges[j][0])
    return connections

def win_check(connections, k):
    # --------------------------------------------
    # funkcja sprawdza czy graf ma k klikę
    #
    # in:
    # connections - lista wierzchołków sąsiednich do
    # wierzchołka i
    # k - rozmiar szukanej kilki
    #
    # out:
    # bool tego czy jest klika
    # --------------------------------------------
    for i in range(len(connections)):
        counter = 0
        for j in range(len(connections)):
            if (len(connections[j]) >= k) & (set(connections[i]).issubset(set(connections[j]))):
                counter += 1
        if counter >= k:
            return True
    return False

def find_best(G, G2, G1):
    # --------------------------------------------
    # funkcja szuka najlepszej możliwej krawędzi
    # do pokolorowania przez server
    #
    # in:
    # G1 - graf z krawędziami gracza
    # G2 - graf z krawędziami servera
    # G - graf z krawędziami dostępnymi do wzięcia
    # na razie trzeba podać k - rozmiar kliki
    # na razie k = 3
    #
    # out:
    # edge - indeks najleszpej krawędzi w liście
    # niezajętych jeszcze krawędzi
    # to trzeba pewnie zmienić żeby zwracało
    # krawędź w takiej postaci jak jest
    # przechowywana na froncie
    #
    # To do:
    # Trzeba wywalić dane wejściowe
    # były mi potrzebne do testowania ale wszystko
    # pewnie da się wziąść z frontendu
    # Trzeba będzie napisać funkcje która weźmie
    # graf z frontendu i rozbije go na G1 i G2,
    # G w zasadzie nie jest potrzebny listę
    # niezajętych krawędzi można o wiele łatwiej
    # zdobyć w inny sposób
    # --------------------------------------------

    k = 3
    
    losing_edge = 0
    for i in range(len(list(G.edges))):
        edge = list(G.edges)[i]
        G2.add_edge(*edge)
        if win_check(connect(G2), k):
            G2.remove_edge(*edge)
            return i
        G2.remove_edge(*edge)
        if losing_edge == 0:
            G1.add_edge(*edge)
            if win_check(connect(G1), k):
                losing_edge = i
            G1.remove_edge(*edge)
    return losing_edge

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

    edges = request.json.get('data').get('graph').get('edges')

    available_edges = list(filter(lambda x: "style" not in x, edges))

    random_edge = random.choice(available_edges)

    return random_edge
