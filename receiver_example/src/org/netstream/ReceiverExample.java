import java.io.IOException;
import java.net.UnknownHostException;

import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.MultiGraph;
import org.graphstream.stream.netstream.NetStreamReceiver;
import org.graphstream.stream.thread.ThreadProxyPipe;

/**
 *  A simple example of use of the NetStream receiver.
 */
public class ReceiverExample {

    public static void main(String[] args) throws UnknownHostException, IOException, InterruptedException {
        // ----- On the receiver side -----
        //
        // - a graph that will display the received events
        Graph g = new MultiGraph("G");
        g.display();
        // - the receiver that waits for events
        NetStreamReceiver net = new NetStreamReceiver(2001);
        net.setDebugOn(true);
        // - received events end up in the "default" pipe
        ThreadProxyPipe pipe = net.getDefaultStream();
        // - plug the pipe to the sink of the graph
        pipe.addSink(g);
        // -The receiver pro-actively checks for events on the ThreadProxyPipe
        while (true) {
            pipe.pump();
            Thread.sleep(100);
        }
    }
}