import socket
import struct

from netstream_constants import *

HOST = 'localhost'
PORT = 2001
STREAM_ID="default"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#stream
stream =struct.pack("!i",len(STREAM_ID))+STREAM_ID

#event add node
event= struct.pack("!bi", EVENT_ADD_NODE, len("n0"))+"n0"
s.sendall(struct.pack("!i",+len(stream)+len(event))+stream+event)

#event add node
event= struct.pack("!bi", EVENT_ADD_NODE, len("n1"))+"n1"
s.sendall(struct.pack("!i",+len(stream)+len(event))+stream+event)

#event add edge
event= struct.pack("!bi", EVENT_ADD_EDGE, len("edge"))+"edge"+struct.pack("!i",len("n1"))+"n1"+struct.pack("!i",len("n0"))+"n0"+struct.pack("!b",0)
s.sendall(struct.pack("!i",+len(stream)+len(event))+stream+event)




#s.close()
