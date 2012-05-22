import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ConnectException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;

import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.MultiGraph;
import org.graphstream.stream.netstream.NetStreamSender;
import org.graphstream.stream.netstream.packing.Base64Packer;

/**
 *
 * Copyright (c) 2012 University of Le Havre
 *
 * @file W3SinkTest.java
 * @date May 16, 2012
 *
 * @author Yoann Pigné
 *
 */

/**
 * 
 */
public class Test1 {
	String clientSentence;
    String capitalizedSentence;
    
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		new Test1();
	}
	public Test1() throws IOException{
		ServerSocket welcomeSocket = new ServerSocket(2001);
		System.out.println("Listening?..."); 
        while(true)
        {
           Socket connectionSocket = welcomeSocket.accept();
           BufferedReader inFromClient =
              new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
           //DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
           clientSentence = inFromClient.readLine();
           System.out.println("Received: " + clientSentence);
           new Thread(){
			@Override
			public void run() {
				try {
					sendGraph(new Integer(clientSentence));
				} catch (NumberFormatException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}        	   
           }.start();
           
        }


	}
	public void sendGraph(int port) throws IOException{
		Graph g = new MultiGraph("G");
		// - the sender
		NetStreamSender nsc = null;
		try {
			System.err.printf("Trying to connect to port %d%n",port);
			nsc = new NetStreamSender("D", "localhost", port);
		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch(Exception e){
			e.printStackTrace();
			return;	
		}
		System.err.printf("connected%n");
		System.err.printf("sending...%n");
		nsc.setPacker(new Base64Packer());

		// - plug the graph to the sender so that graph events can be
		// sent automatically
		g.addSink(nsc);
		// - generate some events on the client side
		String style = "node{fill-mode:plain;fill-color:#567;size:6px;}";
		g.addAttribute("stylesheet", style);
		for (int i = 0; i < 5000; i++) {
			try {
				//Thread.sleep(500);
			} catch (Exception e) {
				e.printStackTrace();
			}
			g.addNode("n"+i);
			if (i > 0) {
				g.addEdge("n"+i + "_" + "n"+(i - 1), "n"+i, "n"+(i - 1));
				g.addEdge("n"+i + "__" + "n"+(i / 2), "n"+i , "n"+(i / 2));
			}
		}
		g.write("ok.dgs");
		System.err.printf("Done.");
	}

}
