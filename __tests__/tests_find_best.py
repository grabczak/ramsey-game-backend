import pytest
import networkx as nx
from graph_logic import find_best


def test_find_best1():
    # random test graph is not complete
    edges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "browser"},
        {"id": "2-3", "source": 2, "target": 3, "team": "server"},
        {"id": "1-3", "source": 1, "target": 3, "team": "browser"},
        {"id": "1-4", "source": 1, "target": 4, "team": "none"},
        {"id": "2-4", "source": 2, "target": 4, "team": "none"},
        # {"id": "3-4", "source": 3, "target": 4, "team": "none"},
    ]
    result = find_best(edges, 3)
    assert result["winner"] == "none"
    assert result["edge"] == {"id": "1-4", "source": 1, "target": 4, "team": "none"}
    assert result["clique"] == []


def test_find_best2():
    edges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "none"},
        {"id": "1-3", "source": 1, "target": 3, "team": "none"},
        {"id": "1-4", "source": 1, "target": 4, "team": "none"},
        {"id": "1-5", "source": 1, "target": 5, "team": "none"},
        {"id": "1-6", "source": 1, "target": 6, "team": "none"},
        {"id": "2-4", "source": 2, "target": 4, "team": "none"},
        {"id": "2-3", "source": 2, "target": 3, "team": "none"},
        {"id": "2-5", "source": 2, "target": 5, "team": "none"},
        {"id": "2-6", "source": 2, "target": 6, "team": "none"},
        {"id": "3-4", "source": 3, "target": 4, "team": "none"},
        {"id": "3-5", "source": 3, "target": 5, "team": "none"},
        {"id": "3-6", "source": 3, "target": 6, "team": "none"},
        {"id": "4-5", "source": 4, "target": 5, "team": "none"},
        {"id": "4-6", "source": 4, "target": 6, "team": "none"},
        {"id": "5-6", "source": 5, "target": 6, "team": "none"},
    ]
    result = find_best(edges, 3)
    assert result["winner"] == "none"
    assert result["edge"] == {"id": "1-2", "source": 1, "target": 2, "team": "none"}
    assert result["clique"] == []


def test_find_best3():
    # browser won
    edges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "browser"},
        {"id": "1-3", "source": 1, "target": 3, "team": "server"},
        {"id": "1-4", "source": 1, "target": 4, "team": "browser"},
        {"id": "1-5", "source": 1, "target": 5, "team": "server"},
        {"id": "1-6", "source": 1, "target": 6, "team": "none"},
        {"id": "2-3", "source": 2, "target": 3, "team": "none"},
        {"id": "2-4", "source": 2, "target": 4, "team": "browser"},
        {"id": "2-5", "source": 2, "target": 5, "team": "none"},
        {"id": "2-6", "source": 2, "target": 6, "team": "none"},
        {"id": "3-4", "source": 3, "target": 4, "team": "none"},
        {"id": "3-5", "source": 3, "target": 5, "team": "none"},
        {"id": "3-6", "source": 3, "target": 6, "team": "none"},
        {"id": "4-5", "source": 4, "target": 5, "team": "none"},
        {"id": "4-6", "source": 4, "target": 6, "team": "none"},
        {"id": "5-6", "source": 5, "target": 6, "team": "none"},
    ]
    result = find_best(edges, 3)
    assert result["winner"] == "browser"
    win_clique = [
        {"id": "1-2", "source": 1, "target": 2, "team": "browser"},
        {"id": "1-4", "source": 1, "target": 4, "team": "browser"},
        {"id": "2-4", "source": 2, "target": 4, "team": "browser"},
    ]
    assert result["clique"] == win_clique
    assert result["edge"] == None


def test_find_best4():
    # server won
    edges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "none"},
        {"id": "1-3", "source": 1, "target": 3, "team": "none"},
        {"id": "1-4", "source": 1, "target": 4, "team": "none"},
        {"id": "1-5", "source": 1, "target": 5, "team": "server"},
        {"id": "1-6", "source": 1, "target": 6, "team": "server"},
        {"id": "2-3", "source": 2, "target": 3, "team": "none"},
        {"id": "2-4", "source": 2, "target": 4, "team": "browser"},
        {"id": "2-5", "source": 2, "target": 5, "team": "none"},
        {"id": "2-6", "source": 2, "target": 6, "team": "none"},
        {"id": "3-4", "source": 3, "target": 4, "team": "browser"},
        {"id": "3-5", "source": 3, "target": 5, "team": "none"},
        {"id": "3-6", "source": 3, "target": 6, "team": "none"},
        {"id": "4-5", "source": 4, "target": 5, "team": "browser"},
        {"id": "4-6", "source": 4, "target": 6, "team": "none"},
        {"id": "5-6", "source": 5, "target": 6, "team": "none"},
    ]
    result = find_best(edges, 3)
    assert result["winner"] == "server"
    win_clique = [
        {"id": "1-5", "source": 1, "target": 5, "team": "server"},
        {"id": "1-6", "source": 1, "target": 6, "team": "server"},
        {"id": "5-6", "source": 5, "target": 6, "team": "server"},
    ]
    assert result["clique"] == win_clique
    assert result["edge"] == {"id": "5-6", "source": 5, "target": 6, "team": "none"}


def test_find_best5():
    # server blocks browser
    edges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "server"},
        {"id": "1-3", "source": 1, "target": 3, "team": "none"},
        {"id": "1-4", "source": 1, "target": 4, "team": "browser"},
        {"id": "1-5", "source": 1, "target": 5, "team": "none"},
        {"id": "1-6", "source": 1, "target": 6, "team": "browser"},
        {"id": "2-3", "source": 2, "target": 3, "team": "none"},
        {"id": "2-4", "source": 2, "target": 4, "team": "none"},
        {"id": "2-5", "source": 2, "target": 5, "team": "none"},
        {"id": "2-6", "source": 2, "target": 6, "team": "none"},
        {"id": "3-4", "source": 3, "target": 4, "team": "none"},
        {"id": "3-5", "source": 3, "target": 5, "team": "none"},
        {"id": "3-6", "source": 3, "target": 6, "team": "none"},
        {"id": "4-5", "source": 4, "target": 5, "team": "browser"},
        {"id": "4-6", "source": 4, "target": 6, "team": "server"},
        {"id": "5-6", "source": 5, "target": 6, "team": "none"},
    ]
    result = find_best(edges, 3)
    assert result["winner"] == "none"
    assert result["clique"] == []
    assert result["edge"] == {"id": "1-5", "source": 1, "target": 5, "team": "none"}


def test_find_best6():
    # random test
    edges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "server"},
        {"id": "1-3", "source": 1, "target": 3, "team": "browser"},
        {"id": "1-4", "source": 1, "target": 4, "team": "server"},
        {"id": "1-5", "source": 1, "target": 5, "team": "server"},
        {"id": "1-6", "source": 1, "target": 6, "team": "server"},
        {"id": "2-3", "source": 2, "target": 3, "team": "browser"},
        {"id": "2-4", "source": 2, "target": 4, "team": "browser"},
        {"id": "2-5", "source": 2, "target": 5, "team": "browser"},
        {"id": "2-6", "source": 2, "target": 6, "team": "server"},
        {"id": "3-4", "source": 3, "target": 4, "team": "browser"},
        {"id": "3-5", "source": 3, "target": 5, "team": "browser"},
        {"id": "3-6", "source": 3, "target": 6, "team": "none"},
        {"id": "4-5", "source": 4, "target": 5, "team": "none"},
        {"id": "4-6", "source": 4, "target": 6, "team": "none"},
        {"id": "5-6", "source": 5, "target": 6, "team": "none"},
    ]
    result = find_best(edges, 3)
    assert result["winner"] == "browser"
    win_clique = [
        {"id": "2-3", "source": 2, "target": 3, "team": "browser"},
        {"id": "2-4", "source": 2, "target": 4, "team": "browser"},
        {"id": "3-4", "source": 3, "target": 4, "team": "browser"},
    ]
    assert result["clique"] == win_clique
    assert result["edge"] == None


def test_find_best7():
    # draw case - searching for clique 6 in graph which has 6 nodes
    edges = [
        {"id": "1-2", "source": 1, "target": 2, "team": "server"},
        {"id": "1-3", "source": 1, "target": 3, "team": "browser"},
        {"id": "1-4", "source": 1, "target": 4, "team": "server"},
        {"id": "1-5", "source": 1, "target": 5, "team": "server"},
        {"id": "1-6", "source": 1, "target": 6, "team": "server"},
        {"id": "2-3", "source": 2, "target": 3, "team": "browser"},
        {"id": "2-4", "source": 2, "target": 4, "team": "browser"},
        {"id": "2-5", "source": 2, "target": 5, "team": "browser"},
        {"id": "2-6", "source": 2, "target": 6, "team": "server"},
        {"id": "3-4", "source": 3, "target": 4, "team": "browser"},
        {"id": "3-5", "source": 3, "target": 5, "team": "browser"},
        {"id": "3-6", "source": 3, "target": 6, "team": "server"},
        {"id": "4-5", "source": 4, "target": 5, "team": "browser"},
        {"id": "4-6", "source": 4, "target": 6, "team": "server"},
        {"id": "5-6", "source": 5, "target": 6, "team": "browser"},
    ]
    result = find_best(edges, 6)
    assert result["winner"] == "draw"
    assert result["clique"] == []
    assert result["edge"] == None
