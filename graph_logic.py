import networkx as nx

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

    if win_check(browser_graph, k):
        source, target = list(available_edges.edges())[0]
        best_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]
        data = {'edge': best_edge,
                'winner': 'browser'}
        return data 

    losing_edge = 0
    for i in range(len(list(available_edges.edges))):

        edge = list(available_edges.edges)[i]

        server_graph.add_edge(*edge)

        if win_check(server_graph, k):
            server_graph.remove_edge(*edge)
            source, target = edge
            best_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]
            data = {'edge': best_edge,
                    'winner': 'server'}
            return data
        
        server_graph.remove_edge(*edge)

        if losing_edge == 0:
            browser_graph.add_edge(*edge)

            if win_check(browser_graph, k):
                losing_edge = i

            browser_graph.remove_edge(*edge)

    found_edge = list(available_edges.edges())[losing_edge]
    
    source, target = found_edge
    best_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]

    data = {'edge': best_edge,
            'winner': 'none'}

    return data

def json_to_networkx(jedges):
    # --------------------------------------------
    # funkcja konwertująca graf z frontendu do grafu
    # w postaci networkx
    # --------------------------------------------

    nxgraph = nx.Graph()
    for i in range(len(jedges)):
        nxgraph.add_edge(int(jedges[i]["source"]), int(jedges[i]["target"]), team = jedges[i]["team"])
    return nxgraph