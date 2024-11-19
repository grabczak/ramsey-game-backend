import pytest
import networkx as nx
from graph_logic import filter_nxgraph


def tests_filter_nxgraph1():
    # empty graph
    nxgraph = nx.Graph()

    filtered_graph = filter_nxgraph(nxgraph, "A")

    assert len(filtered_graph.nodes) == 0
    assert len(filtered_graph.edges) == 0


def tests_filter_nxgraph2():
    # in result there should be returned empty graph with 3 nodes
    nxgraph = nx.Graph()
    nxgraph.add_edge(1, 2, team="A")
    nxgraph.add_edge(2, 3, team="B")

    filtered_graph = filter_nxgraph(nxgraph, "C")

    assert len(filtered_graph.nodes) == 3
    assert len(filtered_graph.edges) == 0


def tests_filter_graph3():
    # an edge is in wrong format
    nxgraph = nx.Graph()
    nxgraph.add_edge(1, 2)
    nxgraph.add_edge(2, 3, team="A")
    nxgraph.add_edge(3, 4, team="b")
    nxgraph.add_edge(2, 10)

    with pytest.raises(KeyError):
        filter_nxgraph(nxgraph, "A")


def tests_filter_nxgraph4():
    # graph with diffrent teams
    nxgraph = nx.Graph()
    nxgraph.add_edge(1, 2, team="A")
    nxgraph.add_edge(2, 3, team="B")
    nxgraph.add_edge(3, 4, team="C")
    nxgraph.add_edge(1, 4, team="C")
    nxgraph.add_edge(2, 4, team="C")

    filtered_graph_a = filter_nxgraph(nxgraph, "A")
    filtered_graph_b = filter_nxgraph(nxgraph, "B")
    filtered_graph_c = filter_nxgraph(nxgraph, "C")

    assert len(filtered_graph_a.edges) == 1
    assert (1, 2) in filtered_graph_a.edges

    assert len(filtered_graph_b.edges) == 1
    assert (2, 3) in filtered_graph_b.edges

    assert len(filtered_graph_c.edges) == 3
    assert (3, 4) in filtered_graph_c.edges
    assert (1, 4) in filtered_graph_c.edges
    assert (2, 4) in filtered_graph_c.edges


def tests_filter_nxgraph5():
    nxgraph = nx.Graph()
    nxgraph.add_edge(1, 1, team="A")
    nxgraph.add_edge(1, 2, team="B")
    nxgraph.add_edge(2, 3, team="A")
    nxgraph.add_edge(3, 4, team="A")
    filtered_graph = filter_nxgraph(nxgraph, "A")

    assert len(filtered_graph.nodes) == 4
    assert len(filtered_graph.edges) == 3
    assert (1, 1) in filtered_graph.edges
    assert (2, 3) in filtered_graph.edges
    assert (3, 4) in filtered_graph.edges
