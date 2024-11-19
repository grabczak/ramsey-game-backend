import pytest
from graph_logic import create_json_edge


def tests_create_json_edge1():

    json_edge = create_json_edge(1, 2, "browser")

    assert json_edge["id"] == "1-2"
    assert json_edge["source"] == 1
    assert json_edge["target"] == 2
    assert json_edge["team"] == "browser"


def tests_create_json_edge2():

    json_edge = create_json_edge(2, 3, "server")

    assert json_edge["id"] == "2-3"
    assert json_edge["source"] == 2
    assert json_edge["target"] == 3
    assert json_edge["team"] == "server"


def tests_create_json_edge3():
    # test without argument team
    json_edge = create_json_edge(3, 4)

    assert json_edge["id"] == "3-4"
    assert json_edge["source"] == 3
    assert json_edge["target"] == 4
    assert json_edge["team"] == "none"


def tests_create_json_edge4():
    # test with only 1 argument

    with pytest.raises(TypeError):
        create_json_edge(2)
