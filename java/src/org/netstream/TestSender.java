package org.netstream;

import java.io.IOException;

/**
 * Created by kraemerb on 25.02.2015.
 */
public class TestSender {
    public static void main(String[] args) throws IOException {
        final String sourceId = "C++_netstream_test";
        long timeId = 0L;
        NetStreamSender stream = new NetStreamSender("localhost", 2001);
        stream.graphCleared(sourceId, timeId++);
        stream.close();
    }
}
