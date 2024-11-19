import pytest
import networkx as nx
from graph_logic import win_check


def test_win_check1():
    # empty graph should causes a value error
    G = nx.Graph()
    with pytest.raises(ValueError):
        win_check(G, 2)


def test_win_check2():
    # complete graph with 6 nodes
    G = nx.complete_graph(6)
    result, clique = win_check(G, 6)
    assert result == True
    assert set(clique) == {0, 1, 2, 3, 4, 5}


def test_win_check3():
    # complete graph with 6 nodes
    # searching for clique of 3
    G = nx.complete_graph(6)
    result, clique = win_check(G, 3)
    assert result == True
    assert clique == [0, 1, 2, 3, 4, 5]


def test_win_check4():
    graph = nx.Graph()
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (4, 5), (4, 5), (5, 1)]
    graph.add_edges_from(edges)
    result, clique = win_check(graph, 3)
    assert result == True
    assert clique == [0, 1, 2]


def test_win_check5():
    # Graph with 7 nodes
    graph = nx.Graph()
    edges = [
        (0, 1),
        (1, 2),
        (1, 3),
        (0, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (0, 6),
        (2, 4),
    ]
    graph.add_edges_from(edges)
    result, clique = win_check(graph, 5)
    assert result == False
    assert clique == [0, 1, 2]


def test_win_check6():
    G = nx.complete_graph(7)
    result, clique = win_check(G, 10)
    assert result == False
    assert set(clique) == {0, 1, 2, 3, 4, 5, 6}
