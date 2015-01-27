import logging
from gs_netstream.sender import  NetStreamProxyGraph, NetStreamSender

logging.basicConfig(level=logging.DEBUG)

sender = NetStreamSender(2012)
proxy = NetStreamProxyGraph(sender)

style = "node{fill-mode:plain;fill-color:gray;size:1px;}"
proxy.add_attribute("stylesheet", style)

proxy.add_attribute("ui.antialias", True)
proxy.add_attribute("layout.stabilization-limit", 0)

for i in range(0,500):
    proxy.add_node(str(i))
    if i > 0:
        proxy.add_edge(str(i) + "_" + str(i-1), str(i), str(i-1), False)
        proxy.add_edge(str(i) + "__" + str(i/2), str(i), str(i/2), False)
