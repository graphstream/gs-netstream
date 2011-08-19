import socket
import struct

CMD_DEL_EDGE=0x13

HOST = 'localhost'
PORT = 2001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


mid="ab"
msg= struct.pack("!Bh", 255, len(mid))+mid
s.send(msg)





s.close()
