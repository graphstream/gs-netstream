/*
 * Copyright 2006 - 2013
 *     Stefan Balev     <stefan.balev@graphstream-project.org>
 *     Julien Baudry    <julien.baudry@graphstream-project.org>
 *     Antoine Dutot    <antoine.dutot@graphstream-project.org>
 *     Yoann Pigné      <yoann.pigne@graphstream-project.org>
 *     Guilhelm Savin   <guilhelm.savin@graphstream-project.org>
 * 
 * This file is part of GraphStream <http://graphstream-project.org>.
 * 
 * GraphStream is a library whose purpose is to handle static or dynamic
 * graph, create them from scratch, file or any source and display them.
 * 
 * This program is free software distributed under the terms of two licenses, the
 * CeCILL-C license that fits European law, and the GNU Lesser General Public
 * License. You can  use, modify and/ or redistribute the software under the terms
 * of the CeCILL-C license as circulated by CEA, CNRS and INRIA at the following
 * URL <http://www.cecill.info> or under the terms of the GNU LGPL as published by
 * the Free Software Foundation, either version 3 of the License, or (at your
 * option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
 * PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * The fact that you are presently reading this means that you have had
 * knowledge of the CeCILL-C and LGPL licenses and that you accept their terms.
 */
 
/**
 * Copyright (c) 2015 Technische Universtität München, Germany
 *
 * NetStreamSender.cs
 * @since Feb 25, 2015
 *
 * @author Benjamin Krämer <benjamin.kraemer@in.tum.de>
 *
 */
using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Netstream
{
    internal class NetStreamSender
    {
        private readonly byte[] _streamIdArray;
        private readonly String _host;
        private readonly int _port;
        private Socket _socket;
        private BufferedStream _outStream;
        private NetStreamPacker _packer = new DefaultPacker();

        private class DefaultPacker : NetStreamPacker
        {
            private readonly NetStreamStorage _sizeBuffer = new NetStreamStorage(sizeof (int));

            public override NetStreamStorage PackMessage(NetStreamStorage buffer, int startIndex, int endIndex)
            {
                return buffer;
            }

            public override NetStreamStorage PackMessageSize(int capacity)
            {
                _sizeBuffer.Position = 0;
                byte[] bytes = BitConverter.GetBytes(capacity);
                if (BitConverter.IsLittleEndian)
                    Array.Reverse(bytes);
                _sizeBuffer.Write(bytes, 0, bytes.Length);
                return _sizeBuffer;
            }

        };

        public NetStreamSender(int port)
            : this("default", "localhost", port)
        {

        }

        public NetStreamSender(String host, int port)
            : this("default", host, port)
        {
        }

        public NetStreamSender(String stream, String host, int port)
        {
            _host = host;
            _port = port;
            _streamIdArray = Encoding.UTF8.GetBytes(stream);

            Connect();
        }

        /**
         * Sets an optional NetStreamPaker whose "pack" method will be called on
         * each message.
         * 
         * a Packer can do extra encoding on the all byte array message, it may also
         * crypt things.
         * 
         * @param paker
         *            The packer object
         */

        public void SetPacker(NetStreamPacker paker)
        {
            _packer = paker;
        }

        public void RemovePacker()
        {
            _packer = new DefaultPacker();
        }

        protected void Connect()
        {
            _socket = new Socket(SocketType.Stream, ProtocolType.Tcp);
            _socket.Connect(new DnsEndPoint(_host, _port));
            _outStream = new BufferedStream(new NetworkStream(_socket));
        }

        /**
         * @param buff
         */

        private void DoSend(NetStreamStorage buff)
        {
            if (!_socket.Connected)
            {
                Console.Error.WriteLine("NetStreamSender : can't send. The socket is closed.");
            }
            else
            {
                buff.Flip();
                NetStreamStorage buffer = _packer.PackMessage(buff);
                NetStreamStorage sizeBuffer = _packer.PackMessageSize(buffer.Capacity);
                buff.Position = 0;

                // real sending
                try
                {
                    _outStream.Write(sizeBuffer.ToArray(), 0, sizeBuffer.Capacity);
                    _outStream.Write(buffer.ToArray(), 0, buffer.Capacity);
                    _outStream.Flush();
                }
                catch (IOException e)
                {
                    Console.Error.WriteLine(e.StackTrace);
                }
            }
        }

        protected void AddAttribute(String sourceId, ulong timeId, String attribute, Object value, NetStreamEvent e)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(e).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeString(attribute).
                EncodeValueWithType(value);
            DoSend(buff);
        }

        protected void ChangeAttribute(String sourceId, ulong timeId, String attribute, Object oldValue, Object newValue,
            NetStreamEvent e)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(e).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeString(attribute).
                EncodeValueWithType(oldValue).
                EncodeValueWithType(newValue);
            DoSend(buff);
        }

        protected void RemoveAttribute(String sourceId, ulong timeId, String attribute, NetStreamEvent e)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(e).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeString(attribute);
            DoSend(buff);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#graphAttributeAdded(java.lang.String
         * , long, java.lang.String, java.lang.Object)
         */
        public void AddGraphAttribute(String sourceId, ulong timeId, String attribute, Object value)
        {
            AddAttribute(sourceId, timeId, attribute, value, NetStreamEvent.AddGraphAttr);
        }

        /*
	     * (non-Javadoc)
	     * 
	     * @see
	     * org.graphstream.stream.AttributeSink#graphAttributeChanged(java.lang.
	     * String, long, java.lang.String, java.lang.Object, java.lang.Object)
	     */
        public void ChangeGraphAttribute(String sourceId, ulong timeId, String attribute, Object oldValue,
            Object newValue)
        {
            ChangeAttribute(sourceId, timeId, attribute, oldValue, newValue, NetStreamEvent.ChgGraphAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#graphAttributeRemoved(java.lang.
         * String, long, java.lang.String)
         */
        public void RemoveGraphAttribute(String sourceId, ulong timeId, String attribute)
        {
            RemoveAttribute(sourceId, timeId, attribute, NetStreamEvent.DelGraphAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#nodeAttributeAdded(java.lang.String,
         * long, java.lang.String, java.lang.String, java.lang.Object)
         */
        public void AddNodeAttribute(String sourceId, ulong timeId, String nodeId,
            String attribute, Object value)
        {
            AddAttribute(sourceId, timeId, attribute, value, NetStreamEvent.AddNodeAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#nodeAttributeChanged(java.lang.String
         * , long, java.lang.String, java.lang.String, java.lang.Object,
         * java.lang.Object)
         */
        public void ChangeNodeAttribute(String sourceId, ulong timeId,
            String nodeId, String attribute, Object oldValue, Object newValue)
        {
            ChangeAttribute(sourceId, timeId, attribute, oldValue, newValue, NetStreamEvent.ChgNodeAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#nodeAttributeRemoved(java.lang.String
         * , long, java.lang.String, java.lang.String)
         */
        public void RemoveNodeAttribute(String sourceId, ulong timeId,
            String nodeId, String attribute)
        {
            RemoveAttribute(sourceId, timeId, attribute, NetStreamEvent.DelNodeAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#edgeAttributeAdded(java.lang.String,
         * long, java.lang.String, java.lang.String, java.lang.Object)
         */
        public void AddEdgeAttribute(String sourceId, ulong timeId, String edgeId,
            String attribute, Object value)
        {
            AddAttribute(sourceId, timeId, attribute, value, NetStreamEvent.AddEdgeAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#edgeAttributeChanged(java.lang.String
         * , long, java.lang.String, java.lang.String, java.lang.Object,
         * java.lang.Object)
         */
        public void ChangeEdgeAttribute(String sourceId, ulong timeId,
            String edgeId, String attribute, Object oldValue, Object newValue)
        {
            ChangeAttribute(sourceId, timeId, attribute, oldValue, newValue, NetStreamEvent.ChgEdgeAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see
         * org.graphstream.stream.AttributeSink#edgeAttributeRemoved(java.lang.String
         * , long, java.lang.String, java.lang.String)
         */
        public void RemoveEdgeAttribute(String sourceId, ulong timeId,
            String edgeId, String attribute)
        {
            RemoveAttribute(sourceId, timeId, attribute, NetStreamEvent.DelEdgeAttr);
        }

        /*
         * (non-Javadoc)
         * 
         * @see org.graphstream.stream.ElementSink#nodeAdded(java.lang.String, long,
         * java.lang.String)
         */
        public void AddNode(String sourceId, ulong timeId, String nodeId)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(NetStreamEvent.AddNode).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeString(nodeId);
            DoSend(buff);
        }

        /*
         * (non-Javadoc)
         * 
         * @see org.graphstream.stream.ElementSink#nodeRemoved(java.lang.String,
         * long, java.lang.String)
         */
        public void RemoveNode(String sourceId, ulong timeId, String nodeId)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(NetStreamEvent.DelNode).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeString(nodeId);
            DoSend(buff);
        }

        /*
         * (non-Javadoc)
         * 
         * @see org.graphstream.stream.ElementSink#edgeAdded(java.lang.String, long,
         * java.lang.String, java.lang.String, java.lang.String, boolean)
         */
        public void AddEdge(String sourceId, ulong timeId, String edgeId,
            String fromNodeId, String toNodeId, bool directed)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(NetStreamEvent.AddEdge).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeString(edgeId).
                EncodeString(fromNodeId).
                EncodeString(toNodeId).
                EncodeNative(directed);
            DoSend(buff);
        }

        /*
         * (non-Javadoc)
         * 
         * @see org.graphstream.stream.ElementSink#edgeRemoved(java.lang.String,
         * long, java.lang.String)
         */
        public void RemoveEdge(String sourceId, ulong timeId, String edgeId)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(NetStreamEvent.DelEdge).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeString(edgeId);
            DoSend(buff);
        }

        /*
         * (non-Javadoc)
         * 
         * @see org.graphstream.stream.ElementSink#graphCleared(java.lang.String,
         * long)
         */
        public void GraphClear(String sourceId, ulong timeId)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(NetStreamEvent.Cleared).
                EncodeString(sourceId).
                EncodeNative(timeId);
            DoSend(buff);
        }

        /*
         * (non-Javadoc)
         * 
         * @see org.graphstream.stream.ElementSink#stepBegins(java.lang.String,
         * long, double)
         */
        public void StepBegins(String sourceId, ulong timeId, double step)
        {
            NetStreamStorage buff = new NetStreamStorage().
                EncodeArray(_streamIdArray).
                EncodeEvent(NetStreamEvent.Step).
                EncodeString(sourceId).
                EncodeNative(timeId).
                EncodeNative(step);
            DoSend(buff);
        }

        /**
         * Force the connection to close (properly) with the server
         * 
         * @throws IOException
         */
        public void Close()
        {
            _socket.Close();
        }
    }
}
