/**
 *
 *
 * Copyright (c) 2010-2011 University of Luxembourg
 *
 *
 * @file client_socket.h
 * @date 2011-08-21
 *
 * @author Yoann Pigné
 */
 
 #ifndef CLIENT_SOCKET_H
 #define CLIENT_SOCKET_H
 class ClientSocket{
   
 public:
   ClientSocket();
   Initialize();
   void SetNonBloking();
   void Open(const string & host, int port);
   int Send((uint8 *) data, int size);
   int Receive(int limit);
   
   
 }
 
 #endif // CLIENT_SOCKET_H