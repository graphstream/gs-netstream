"""Proxy Netstream graph class"""


class NetStreamProxyGraph:
    """
    This is a utility class that handles 'source id' and 'time id' synchronization tokens.
    It proposes utile classes that allow to directly send events through the network pipe.
    """

    def __init__(self, sender, source_id=None):
        """Constructor can be with one NetStreamSender object and a source id OR with with 4 args.

        Notes:
            4 args: Source ID, Stream ID, Host, and port number
        """
        self.sender = sender
        self.source_id = source_id if source_id else "nss%d" % (1000 * random())
        self.time_id = 0

    def run_sender_method(self, sender_method, *args, **kwargs):
        sender_method(self.source_id, self.time_id, *args, **kwargs)
        self.time_id += 1

    def add_node(self, node: str):
        """Add a node to the graph."""
        self.run_sender_method(self.sender.node_added, node)

    def remove_node(self, node: str):
        """Remove a node from the graph."""
        self.run_sender_method(self.sender.node_removed, node)

    def add_edge(self, edge: str, from_node: str, to_node: str, directed: bool = False):
        """Add an edge to the graph."""
        self.run_sender_method(self.sender.edge_added, edge, from_node, to_node, directed)

    def remove_edge(self, edge: str):
        """Remove an edge from the graph."""
        self.run_sender_method(self.sender.edge_removed, edge)

    def add_attribute(self, attribute: str, value):
        """Add an attribute to the graph."""
        self.run_sender_method(self.sender.graph_attribute_added, attribute, value)

    def remove_attribute(self, attribute: str):
        """Remove an attribute from the graph."""
        self.run_sender_method(self.sender.graph_attribute_removed, attribute)

    def change_attribute(self, attribute: str, old_value, new_value):
        """Change an attribute of the graph."""
        self.run_sender_method(self.sender.graph_attribute_changed, attribute, old_value, new_value)

    def add_node_attribute(self, node: str, attribute: str, value):
        """Add an attribute to a node."""
        self.run_sender_method(self.sender.node_attribute_added, node, attribute, value)

    def remove_node_attibute(self, node: str, attribute: str):
        """Remove an attribute from a node."""
        self.run_sender_method(self.sender.node_attribute_removed, node, attribute)

    def change_node_attribute(self, node: str, attribute: str, old_value, new_value):
        """Change an attribute of a node."""
        self.run_sender_method(self.sender.node_attribute_changed, node, attribute, old_value, new_value)

    def add_edge_attribute(self, edge: str, attribute: str, value):
        """Add an attribute to an edge."""
        self.run_sender_method(self.sender.edge_attribute_added, edge, attribute, value)

    def remove_edge_attribute(self, edge: str, attribute: str):
        """Remove an attribute from an edge."""
        self.run_sender_method(self.sender.edge_attribute_removed, edge, attribute)

    def change_edge_attribute(self, edge: str, attribute: str, old_value, new_value):
        """Change an attribute of an edge."""
        self.run_sender_method(self.sender.edge_attribute_changed, edge, attribute, old_value, new_value)

    def clear_graph(self):
        """Clear the graph."""
        self.run_sender_method(self.sender.graph_cleared)

    def step_begins(self, time: int):
        """Begin a step."""
        self.run_sender_method(self.sender.step_begun, time)
