import networkx as nx


def win_check(graph, k):
    clique = max(nx.find_cliques(graph), key=len)

    return (len(clique) >= k, sorted(clique))


def find_best(edges, k):
    nxgraph = json_to_networkx(edges)

    browser_graph = filter_nxgraph(nxgraph, "browser")
    server_graph = filter_nxgraph(nxgraph, "server")
    available_edges = filter_nxgraph(nxgraph, "none")

    check, clique = win_check(browser_graph, k)

    if check:
        clique_edges = clique_to_json(clique, "browser")

        data = {"edge": None, "winner": "browser", "clique": clique_edges}
        return data

    if len(list(available_edges.edges())) <= 1:
        if len(list(available_edges.edges())) == 1:
            source, target = list(available_edges.edges())[0]
            last_edge = create_json_edge(source, target)
        else:
            last_edge = None

        data = data = {"edge": last_edge, "winner": "draw", "clique": []}
        return data

    losing_edge = 0
    for i in range(len(list(available_edges.edges))):
        edge = list(available_edges.edges)[i]

        server_graph.add_edge(*edge)

        check, clique = win_check(server_graph, k)

        if check:
            server_graph.remove_edge(*edge)

            source, target = edge
            best_edge = create_json_edge(source, target)
            clique_edges = clique_to_json(clique, "server")

            data = {"edge": best_edge, "winner": "server", "clique": clique_edges}

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

    best_edge = create_json_edge(source, target)

    data = {"edge": best_edge, "winner": "none", "clique": []}

    return data


def json_to_networkx(jedges):
    nxgraph = nx.Graph()

    for i in range(len(jedges)):
        nxgraph.add_edge(
            int(jedges[i]["source"]), int(jedges[i]["target"]), team=jedges[i]["team"]
        )

    return nxgraph


def clique_to_json(nodes, team):
    jedges = []

    for i in range(len(nodes) - 1):
        for j in list(range(i + 1, len(nodes))):
            edge = create_json_edge(nodes[i], nodes[j], team)
            jedges.append(edge)

    return jedges


def create_json_edge(source, target, team="none"):

    jedge = {
        "id": f"{source}-{target}",
        "source": source,
        "target": target,
        "team": team,
    }

    return jedge


def filter_nxgraph(nxgraph, filter):
    filtered_graph = nx.Graph()

    filtered_graph.add_nodes_from(list(nxgraph.nodes))

    filtered_graph.add_edges_from(
        [(u, v) for u, v, e in nxgraph.edges(data=True) if e["team"] == filter]
    )
    return filtered_graph
