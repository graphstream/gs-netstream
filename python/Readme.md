# Python example of the NetStreamGraph usage

For running NetStreamGraph on python you need to do the following:
1. Run a server receiver for graph visualization.
   
    [Java server example](https://github.com/max-kalganov/graph_stream_server)
2. Use NetStreamProxyGraph to fill a graph. 
   
   class import - `from gs_netstream import NetStreamProxyGraph`
   See NetStreamProxyGraph implementation to look up graph methods.

Run `example_sender.py` for an experiment.