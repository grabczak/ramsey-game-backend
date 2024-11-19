import pytest
from graph_logic import clique_to_json


# function clique_to_json changes nodes and team to graph in json format

def test_clique_to_json1():
    # empty clique    
    result = clique_to_json([], "server")
    assert result == []

def test_clique_to_json2():
    result = clique_to_json([1, 2, 3], "A")
    expected = [
        {"id": "1-2", "source": 1, "target": 2, "team": "A"},
        {"id": "1-3", "source": 1, "target": 3, "team": "A"},
        {"id": "2-3", "source": 2, "target": 3, "team": "A"},
    ]
    assert result == expected


def test_clique_to_json3():
    # only one node i clique expectes empty list of edges
    result = clique_to_json([2], "none")
    assert result == [] 



def test_clique_to_json4():
    #clique of 4 nodes
    result = clique_to_json([1, 2, 3, 4, 5], "browser")
    expected = [
        {"id": "1-2", "source": 1, "target": 2, "team": "browser"},
        {"id": "1-3", "source": 1, "target": 3, "team": "browser"},
        {"id": "1-4", "source": 1, "target": 4, "team": "browser"},
        {"id": "1-5", "source": 1, "target": 5, "team": "browser"},
        {"id": "2-3", "source": 2, "target": 3, "team": "browser"},
        {"id": "2-4", "source": 2, "target": 4, "team": "browser"},
        {"id": "2-5", "source": 2, "target": 5, "team": "browser"},
        {"id": "3-4", "source": 3, "target": 4, "team": "browser"},
        {"id": "3-5", "source": 3, "target": 5, "team": "browser"},
        {"id": "4-5", "source": 4, "target": 5, "team": "browser"},
    ]
    assert result == expected


def tests_clique_to_json5():
    #wrong amount of parameters
    with pytest.raises(TypeError):
        clique_to_json([1, 2, 3])