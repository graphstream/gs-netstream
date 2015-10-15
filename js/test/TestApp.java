import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.DefaultGraph;
import org.graphstream.stream.GraphReplay;
import org.graphstream.stream.netstream.NetStreamReceiver;
import org.graphstream.stream.netstream.NetStreamSender;
import org.graphstream.stream.netstream.packing.Base64Packer;
import org.graphstream.stream.netstream.packing.Base64Unpacker;
import org.graphstream.stream.thread.ThreadProxyPipe;
import org.graphstream.util.VerboseSink;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.LinkedList;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 *
 * Copyright (c) 2012 University of Le Havre
 *
 * @file NetSteamWebSocketTestApp.java
 * @date May 21, 2012
 *
 * @author Yoann Pigné
 *
 */

/**
 *
 */
public class TestApp {
    boolean alive;
    ServerSocket serverSocket;
    Graph g;
    ConcurrentLinkedQueue<Connection> pending;
    LinkedList<Connection> active;

	public TestApp() throws IOException {
		this.serverSocket = new ServerSocket(2001);
		this.alive = true;
		this.pending = new ConcurrentLinkedQueue<Connection>();
		this.g = new DefaultGraph("w3sink-demo",false, true);
    	g.setAutoCreate(true);

		VerboseSink vs = new VerboseSink();
		g.addSink(vs);

		this.active = new LinkedList<Connection>();

        Runnable r = new Runnable() {
        	public void run() {
        		TestApp.this.listen();
        	}
        };

        Thread t = new Thread(r);
        t.setDaemon(true);
        t.start();

        r = new Runnable() {
        	public void run() {
        		try {
					TestApp.this.handleGraph();
				} catch (UnknownHostException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
        	}
        };

        t = new Thread(r);
        t.start();
	}

	private void handleGraph() throws UnknownHostException, IOException {
		System.out.printf(" * graph running ...\n");


		NetStreamReceiver receiver = new NetStreamReceiver("localhost", 2002);
		receiver.setUnpacker(new Base64Unpacker());

		ThreadProxyPipe pipe = receiver.getDefaultStream();

		pipe.addSink(g);


		// send events to clients through node.js
		NetStreamSender sender = new NetStreamSender(2000);
		sender.setPacker(new Base64Packer());
		g.addSink(sender);

		while (alive) {

			// get events from clients
			pipe.pump();

			// get new clients and send replay
			while (pending.size() > 0)
				register(pending.poll());

			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
			}
		}
	}

	private void register(Connection conn) {
		GraphReplay replay = new GraphReplay("replay-" + g.getId());

		replay.addSink(conn.nss);
		replay.replay(g);
		replay.removeSink(conn.nss);

		g.addSink(conn.nss);
		active.add(conn);

		System.out.printf("[generator] new connection registered'\n");
	}

	private void listen() {
		System.out.printf(" * Server is listening ...\n");

		while (alive) {
			Socket s = null;
			Connection c = null;

			try {
				s = serverSocket.accept();
				c = new Connection(s);
				pending.add(c);

				System.out.printf("[server] new connection from '%s'\n", s.getInetAddress().getHostName());
			} catch (IOException e) {
				e.printStackTrace();

				try {
					s.close();
				} catch (IOException e2) {
				}
			}
		}

		try {
			serverSocket.close();
		} catch (Exception e) {
		}

		System.out.printf(" * Server is closed ...\n");
	}

	private class Connection {
		BufferedReader in;
		NetStreamSender nss;

		Connection(Socket socket) throws IOException {
			int port;

			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			port = Integer.parseInt(in.readLine());

			try {
				socket.close();
			} catch (IOException e) {
				e.printStackTrace();
			}

			nss = new NetStreamSender(port);
			nss.setPacker(new Base64Packer());
		}
	}

	/**
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
		new TestApp();
	}


}
