/************************************************************************
 ** This file is part of the network simulator Shawn.                  **
 ** Copyright (C) 2004-2007 by the SwarmNet (www.swarmnet.de) project  **
 ** Shawn is free software; you can redistribute it and/or modify it   **
 ** under the terms of the BSD License. Refer to the shawn-licence.txt **
 ** file in the root of the Shawn source tree for further details.     **
 ************************************************************************/

#ifndef __NETSTREAM_SOCKET_H
#define __NETSTREAM_SOCKET_H


// Get Storage
#ifdef SHAWN
	#include <apps/tcpip/storage.h>
#else
	#include "netstream-storage.h"
#endif

#ifdef SHAWN
     namespace shawn
      { class SimulationController; }

     // Dummy function is called when Shawn Simulation starts. Does nothing up to now.
     extern "C" void init_tcpip( shawn::SimulationController& );
#endif

// Disable exception handling warnings
#ifdef WIN32
	#pragma warning( disable : 4290 )
#endif

#include <string>
#include <map>
#include <vector>
#include <list>
#include <deque>
#include <iostream>


struct in_addr;

namespace netstream
{

	class NetStreamSocketException: public std::exception
	{
	private:
		std::string what_;
	public:
		NetStreamSocketException( std::string what )
		{
			what_ = what;
			//std::cerr << "netstream::NetStreamSocketException: " << what << std::endl << std::flush;
		}

		virtual const char* what() const noexcept
		{
			return what_.c_str();
		}

		~NetStreamSocketException() {}
	};

	class NetStreamSocket
	{
		friend class Response;
	public:
		/// Constructor that prepare to connect to host:port 
		NetStreamSocket(std::string host, int port);
		
		/// Constructor that prepare for accepting a connection on given port
		NetStreamSocket(int port);

		/// Destructor
		~NetStreamSocket();

		/// Connects to host_:port_
		void connect();

		/// Wait for a incoming connection to port_
		void accept();
		void send( const std::vector<unsigned char> ) ;
		void sendExact( const NetStreamStorage & ) ;
		std::vector<unsigned char> receive( int bufSize = 2048 ) ;
		bool receiveExact( NetStreamStorage &) ;
		void close();
		int port();
		void set_blocking(bool) ;
		bool is_blocking() ;
		bool has_client_connection() const;

		// If verbose, each send and received data is written to stderr
		bool verbose() { return verbose_; }
		void set_verbose(bool newVerbose) { verbose_ = newVerbose; }

	private:
		void init();
		void BailOnNetStreamSocketError( std::string ) const ;
#ifdef WIN32
		std::string GetWinsockErrorString(int err) const;
#endif
		bool atoaddr(std::string, struct in_addr& addr);
		bool datawaiting(int sock) const ;

		std::string host_;
		int port_;
		int socket_;
		int server_socket_;
		bool blocking_;

		bool verbose_;
#ifdef WIN32
		static bool init_windows_sockets_;
		static bool windows_sockets_initialized_;
		static int instance_count_;
#endif
	};

}	// namespace tcpip

#endif // BUILD_TCPIP


/*-----------------------------------------------------------------------
* Source  $Source: $
* Version $Revision: 197 $
* Date    $Date: 2008-04-29 17:40:51 +0200 (Tue, 29 Apr 2008) $
*-----------------------------------------------------------------------
* $Log:$
*-----------------------------------------------------------------------*/
