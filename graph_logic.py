import networkx as nx

def win_check(graph, k):    
    clique = max(nx.find_cliques(graph), key = len)
    
    return (len(clique) >= k, clique)


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

    check, clique = win_check(browser_graph, k)

    if check:
        clique_edges = clique_to_json(clique, edges)

        data = {'edge': None,
                'winner': 'browser',
                'clique': clique_edges}
        return data 
    
    if len(list(available_edges.edges())) <= 1:
        if len(list(available_edges.edges())) == 1:
            source, target = list(available_edges.edges())[0]
            last_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]
        else:
            last_edge = None
        data = data = {'edge': last_edge,
                'winner': 'draw',
                'clique': []}
        return data

    losing_edge = 0
    for i in range(len(list(available_edges.edges))):

        edge = list(available_edges.edges)[i]

        server_graph.add_edge(*edge)

        check, clique = win_check(server_graph, k)

        if check:
            server_graph.remove_edge(*edge)
            source, target = edge
            best_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]
            clique_edges = clique_to_json(clique, edges)

            for j in range(len(edges)):
                edges[j]['team'] = 'server'

            data = {'edge': best_edge,
                    'winner': 'server',
                    'clique': clique_edges}
            
            return data
        
        server_graph.remove_edge(*edge)

        if losing_edge == 0:
            browser_graph.add_edge(*edge)

            check, clique = win_check(browser_graph, k)

            if check:
                losing_edge = i

            browser_graph.remove_edge(*edge)

    found_edge = list(available_edges.edges())[losing_edge]
    
    source, target = found_edge

    best_edge = list(filter(lambda x: (int(x.get('source')) == source and int(x.get('target')) == target) or (int(x.get('source')) == target and int(x.get('target')) == source), edges))[0]

    data = {'edge': best_edge,
            'winner': 'none',
            'clique': []}

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

def clique_to_json(nodes, edges):
    jedges = []
    for i in range(len(nodes) - 1):
        for j in list(range(i + 1, len(nodes))):
            edge = list(filter(lambda x: (int(x.get('source')) == nodes[i] and int(x.get('target')) == nodes[j]) or (int(x.get('source')) == nodes[j] and int(x.get('target')) == nodes[i]), edges))[0]
            jedges.append(edge)
    return jedges