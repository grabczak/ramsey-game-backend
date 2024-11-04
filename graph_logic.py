import networkx as nx

# Poniżej archiwalne brednie i herezje.
# Niebawem je usunę ale gdyby ktoś chciał poszperać
# w starym kodzie to na razie zostawiam
#
# Obecnie ta funkcja nie jest potrzebna ale
# na razie tylko zakomentowałem jakby się
# jednak okazało że będzie potrzebna
#
# def connect(Graph): 
#     connections = []
#     nodes = list(Graph.nodes)
#     edges = list(Graph.edges)
#     for i in range(len(nodes)):
#         connections.append([nodes[i]])
#         for j in range(len(edges)):
#             if edges[j][0] == nodes[i]:
#                 connections[i].append(edges[j][1])
#             if edges[j][1] == nodes[i]:
#                 connections[i].append(edges[j][0])
#     return connections


# Wersja 1.0 funkcji sprawdzająca czy gra się skończyła
# na razie zostawiam jakby ktoś chciał się z tym jeszcze
# pomęczyć
#
# def win_check(connections, k):  
#     for i in range(len(connections)):
#         counter = 0
#         for j in range(len(connections)):
#             if (len(connections[j]) >= k) & (set(connections[i]).issubset(set(connections[j]))):
#                 counter += 1
#         if counter >= k:
#             return True
#     return False

def win_check(graph, k):    
    clique = max(nx.find_cliques(graph), key = len)
    
    return len(clique) >= k


def find_best(edges, k):
    # --------------------------------------------
    # funkcja szuka najlepszej możliwej krawędzi
    # do pokolorowania przez server
    #
    # in:
    # edges - krawędzie grafu reprezentującego
    # stan gry
    # k - rozmiar szukanej kliki
    #
    # out:
    # edge - najlepsza krawędź zwracana w formacie 
    # z frontendowego grafu
    # --------------------------------------------

    nxgraph = json_to_networkx(edges)

    browser_graph = nx.Graph([(u, v) for u,v,e in nxgraph.edges(data = True) if e['team'] == 'browser'])
    server_graph = nx.Graph([(u, v) for u,v,e in nxgraph.edges(data = True) if e['team'] == 'server'])
    available_edges = nx.Graph([(u, v) for u,v,e in nxgraph.edges(data = True) if e['team'] == 'none'])

    losing_edge = 0
    for i in range(len(list(available_edges.edges))):

        edge = list(available_edges.edges)[i]

        server_graph.add_edge(*edge)

        if win_check(server_graph, k):
            server_graph.remove_edge(*edge)
            source, target = edge
            best_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]
            return best_edge
        
        server_graph.remove_edge(*edge)

        if losing_edge == 0:
            browser_graph.add_edge(*edge)

            if win_check(browser_graph, k):
                losing_edge = i

            browser_graph.remove_edge(*edge)

    found_edge = list(available_edges.edges())[losing_edge]
    
    source, target = found_edge
    best_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]

    return best_edge



def json_to_networkx(jedges):
    # --------------------------------------------
    # funkcja konwertująca graf z frontendu do grafu
    # w postaci networkx
    # --------------------------------------------

    nxgraph = nx.Graph()
    for i in range(len(jedges)):
        nxgraph.add_edge(int(jedges[i]["source"]), int(jedges[i]["target"]), team = jedges[i]["team"])
    return nxgraph