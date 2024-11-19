import pytest
import networkx as nx
from graph_logic import json_to_networkx

# in shortcut function json_to_networkx converts a list of type
#  { id: "1-2", source: 1, target: 2, team: "none"} to format:
# [ (1, 2, "none"),...]


def test_json_to_networkx1():
    # empty graph
    jedges = []
    graph = json_to_networkx(jedges)

    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0

def test_json_to_networkx2():
    #two egdes
    jedges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "user1"},
        {"id": "2-3", "source": 2, "target": 3, "team": "user2"},
    ]
    graph = json_to_networkx(jedges)

    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2
    assert (1, 2) in graph.edges
    assert graph.edges[1, 2]["team"] == "user1"
    assert graph.edges[2, 3]["team"] == "user2"

def test_json_to_networkx3():
    #only one edge
    jedges = [
        {"id": "2-3", "source": 2, "target": 3, "team": "none"}
    ]
    graph = json_to_networkx(jedges)

    assert len(graph.nodes) == 2
    assert (2, 3) in graph.edges
    assert graph.edges[2, 3]["team"] == "none"


def test_json_to_networkx4():
    # same edges
    jedges = [
        {"id":"1-2", "source": 1, "target": 2, "team": "browser"},
        {"id":"1-2", "source": 1, "target": 2, "team": "browser"},
    ]
    graph = json_to_networkx(jedges)

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1 
    assert graph.edges[1, 2]["team"] == "browser"

def test_json_to_networkx5():
    jedges = [
        {"id":"1-2", "source": 1, "target": 1, "team": "browser"},
        {"id":"1-2", "source": 1, "target": 2, "team": "browser"},
    ]
    graph = json_to_networkx(jedges)

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 2 
    assert graph.edges[1, 2]["team"] == "browser"


def test_json_to_networkx6():
    jedges = [{"id": "{i}-{i+1}", "source": i, "target": i + 1, "team": f"Team {i}"} for i in range(10)]
    graph = json_to_networkx(jedges)

    assert len(graph.nodes) == 11
    assert len(graph.edges) == 10
    assert graph.edges[0, 1]["team"] == "Team 0"
    assert graph.edges[1, 2]["team"] == "Team 1"
    assert graph.edges[2, 3]["team"] == "Team 2"
    assert graph.edges[9, 10]["team"] == "Team 9"
