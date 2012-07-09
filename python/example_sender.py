from gs_netstream.sender import  NetStreamProxyGraph, NetStreamSender, Base64NetStreamTransport

transport = Base64NetStreamTransport("default","localhost",2001)
sender = NetStreamSender(transport)
proxy = NetStreamProxyGraph(sender)

style = "node{fill-mode:plain;fill-color:gray;size:1px;}"
proxy.addAttribute("stylesheet", style)

proxy.addAttribute("ui.antialias", True)
proxy.addAttribute("layout.stabilization-limit", 0)

for i in range(0,500):
 proxy.addNode(str(i))
 if(i>0):
   proxy.addEdge(str(i)+"_"+str(i-1), str(i), str(i-1),False)
   proxy.addEdge(str(i)+"__"+str(i/2), str(i), str(i/2), False)
   