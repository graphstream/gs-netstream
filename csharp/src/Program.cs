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
 * Program.cs
 * @since Feb 25, 2015
 *
 * @author Benjamin Krämer <benjamin.kraemer@in.tum.de>
 *
 */

using System;
using System.Text;
using System.Threading;

namespace Netstream
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            //Endless();
            //EventsTest();
            //TypesTest();
            Example();
        }

        private static void Endless()
        {
            const string sourceId = "C++_netstream_test";
            ulong timeId = 0L;
            var stream = new NetStreamSender("default", "localhost", 2001);
            const string n1 = "node";
            while (timeId < 1000)
            {
                stream.AddNode(sourceId, timeId++, n1 + timeId);
            }
            stream.Close();
        }

        private static void Example()
        {
            const string sourceId = "C++_netstream_test";
            ulong timeId = 0L;
            var stream = new NetStreamSender("default", "localhost", 2001);
            const string style = "node {" +
                " shape: rounded-box;" +
                " fill-color: grey;" +
                " fill-mode: dyn-plain;" +
                " size-mode: fit;" +
                "}" +
                "node.active {" +
                " fill-color: green;" +
                " size:20px;" +
                "}" +
                "edge {" +
                " shape: cubic-curve;" +
                " size: 1px;" +
                " arrow-shape: arrow;" +
                "}" +
                "edge.active {" +
                " fill-color: green;" +
                " size: 5px;" +
                "}";
            stream.AddGraphAttribute(sourceId, timeId++, "stylesheet", style);
            stream.AddGraphAttribute(sourceId, timeId++, "ui.antialias", true);
            stream.AddGraphAttribute(sourceId, timeId++, "ui.quality", true);
            stream.AddGraphAttribute(sourceId, timeId++, "layout.stabilization-limit", 0);
            for (int i = 0; i < 500; i++)
            {
                var n1 = i.ToString();
                AddNodeWithLabel(stream, sourceId, ref timeId, n1);
                if (i > 0)
                {
                    var n2 = (i - 1).ToString();
                    var n3 = (i/2).ToString();
                    var e1 = n1 + "-" + n2;
                    var e2 = n1 + "-" + n3;

                    AddEdgeWithLabel(stream, sourceId, ref timeId, e1, n1, n2);

                    if (!e1.Equals(e2))
                        AddEdgeWithLabel(stream, sourceId, ref timeId, e2, n1, n3);
                }
                //Thread.Sleep(100);
            }
            stream.Close();
        }

        private static String lastEdge, lastNode;
        private static void AddEdgeWithLabel(NetStreamSender stream, string sourceId, ref ulong timeId, string name, string nodeFrom, string nodeTo)
        {
            if (lastEdge != null)
                stream.RemoveEdgeAttribute(sourceId, timeId++, lastEdge, "ui.class");

            stream.AddEdge(sourceId, timeId++, name, nodeFrom, nodeTo, false);
            stream.AddEdgeAttribute(sourceId, timeId++, name, "ui.label", name);
            stream.AddEdgeAttribute(sourceId, timeId++, name, "ui.class", "active");
            lastEdge = name;
        }

        private static void AddNodeWithLabel(NetStreamSender stream, string sourceId, ref ulong timeId, string name)
        {
            if (lastNode != null)
                stream.RemoveNodeAttribute(sourceId, timeId++, lastNode, "ui.class");

            stream.AddNode(sourceId, timeId++, name);
            stream.AddNodeAttribute(sourceId, timeId++, name, "ui.label", name);
            stream.AddNodeAttribute(sourceId, timeId++, name, "ui.class", "active");
            lastNode = name;
        }

        private static void TypesTest()
        {
            const string sourceId = "C++_netstream_test";
            ulong timeId = 0L;
            var stream = new NetStreamSender("default", "localhost", 2001);

            stream.AddGraphAttribute(sourceId, timeId++, "int", 1);
            stream.AddGraphAttribute(sourceId, timeId++, "float", (float) 1);
            stream.AddGraphAttribute(sourceId, timeId++, "double", 1.0);
            stream.AddGraphAttribute(sourceId, timeId++, "long", 1L);
            stream.AddGraphAttribute(sourceId, timeId++, "byte", (char) 0);
            stream.AddGraphAttribute(sourceId, timeId++, "boolean", true);

            int[] v = {1776, 7, 4};
            stream.AddGraphAttribute(sourceId, timeId++, "intArray", v);

            float[] v2 = {1776.3f, 7.3f};
            stream.AddGraphAttribute(sourceId, timeId++, "floatArray", v2);

            double[] v3 = {776.3, .3};
            stream.AddGraphAttribute(sourceId, timeId++, "doubleArray", v3);

            long[] v4 = {1776, 7, 4};
            stream.AddGraphAttribute(sourceId, timeId++, "longArray", v4);

            char[] v5 = {'0', (char) 0, 'z'};
            stream.AddGraphAttribute(sourceId, timeId++, "byteArray", v5);

            bool[] v6 = {true, false};
            stream.AddGraphAttribute(sourceId, timeId++, "booleanArray", v6);

            stream.AddGraphAttribute(sourceId, timeId++, "string", "true");
            stream.Close();
        }

        private static void EventsTest()
        {
            const string sourceId = "C++_netstream_test";
            ulong timeId = 0L;
            var stream = new NetStreamSender("localhost", 2001);
            stream.AddNode(sourceId, timeId++, "node0");
            stream.AddEdge(sourceId, timeId++, "edge", "node0", "node1", true);
            stream.AddNodeAttribute(sourceId, timeId++, "node0", "nodeAttribute", 0);
            stream.ChangeNodeAttribute(sourceId, timeId++, "node0", "nodeAttribute", 0, 1);
            stream.RemoveNodeAttribute(sourceId, timeId++, "node0", "nodeAttribute");
            stream.AddEdgeAttribute(sourceId, timeId++, "edge", "edgeAttribute", 0);
            stream.ChangeEdgeAttribute(sourceId, timeId++, "edge", "edgeAttribute", 0, 1);
            stream.RemoveEdgeAttribute(sourceId, timeId++, "edge", "edgeAttribute");
            stream.AddGraphAttribute(sourceId, timeId++, "graphAttribute", 0);
            stream.ChangeGraphAttribute(sourceId, timeId++, "graphAttribute", 0, 1);
            stream.RemoveGraphAttribute(sourceId, timeId++, "graphAttribute");
            stream.StepBegins(sourceId, timeId++, 1.1);
            stream.RemoveEdge(sourceId, timeId++, "edge");
            stream.RemoveNode(sourceId, timeId++, "node0");
            stream.GraphClear(sourceId, timeId++);
            stream.Close();
        }
    }
}
