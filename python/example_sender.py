import logging
from time import sleep
from gs_netstream import NetStreamProxyGraph
from random import randint

logging.basicConfig(level=logging.DEBUG)


def ex1(graph: NetStreamProxyGraph) -> None:
    style = "node{fill-mode:plain;fill-color:gray;size:1px;}"
    graph.add_attribute("stylesheet", style)

    graph.add_attribute("ui.antialias", True)
    graph.add_attribute("layout.stabilization-limit", 0)

    for i in range(500):
        sleep(0.2)
        graph.add_node(str(i))
        if i > 0:
            graph.add_edge(str(i) + "_" + str(i-1), str(i), str(i-1), False)
            graph.add_edge(str(i) + "__" + str(i/2), str(i), str(i/2), False)


def ex2(graph: NetStreamProxyGraph) -> None:
    graph.add_node("0")
    for i in range(1, 200):
        sleep(0.2)
        graph.add_node(str(i))
        i2 = str(randint(0, i-1))
        graph.add_edge(f"{str(i)}_{i2}", str(i), i2)


if __name__ == '__main__':
    graph = NetStreamProxyGraph(port=8008)
    ex2(graph)
