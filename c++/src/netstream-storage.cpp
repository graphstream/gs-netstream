/************************************************************************
 ** This file is part of the network simulator Shawn.                  **
 ** Copyright (C) 2004-2007 by the SwarmNet (www.swarmnet.de) project  **
 ** Shawn is free software; you can redistribute it and/or modify it   **
 ** under the terms of the BSD License. Refer to the shawn-licence.txt **
 ** file in the root of the Shawn source tree for further details.     **
 ************************************************************************
 **                                                                    **
 ** \author Axel Wegener <wegener@itm.uni-luebeck.de>                  **
 ** \author Bjoern Hendriks <hendriks@ibr.cs.tu-bs.de>                 **
 **                                                                    **
 ************************************************************************/

#include "netstream-storage.h"


#include <iostream>
#include <iterator>
#include <sstream>
#include <cassert>


using namespace std;


namespace netstream
{

	// ----------------------------------------------------------------------
	NetStreamStorage::NetStreamStorage()
	{
		init();
	}


	// ----------------------------------------------------------------------
	NetStreamStorage::NetStreamStorage(unsigned char packet[], int length)
	{
		store.reserve(length);
		// Get the content
		for(int i = 0; i < length; ++i) store.push_back(packet[i]);

		init();
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::init()
	{
		// Initialize local variables
		iter_ = store.begin();

		short a = 0x0102;
		unsigned char *p_a = reinterpret_cast<unsigned char*>(&a);
		bigEndian_ = (p_a[0] == 0x01); // big endian?
	}


	// ----------------------------------------------------------------------
	NetStreamStorage::~NetStreamStorage()
	{}


	// ----------------------------------------------------------------------
	bool NetStreamStorage::valid_pos()
	{
		return (iter_ != store.end());   // this implies !store.empty()
	}


	// ----------------------------------------------------------------------
	unsigned int NetStreamStorage::position() const
	{
		// According to C++ standard std::distance will simply compute the iterators
		// difference for random access iterators as std::vector provides.
		return static_cast<unsigned int>(std::distance(store.begin(), iter_));
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::reset()
	{
		store.clear();
		iter_ = store.begin();
	}


	// ----------------------------------------------------------------------
	/**
	* Reads a char form the array
	* @return The read char (between 0 and 255)
	*/
	unsigned char NetStreamStorage::readChar() 
	{
		if ( !valid_pos() )
		{
			throw std::invalid_argument("NetStreamStorage::readChar(): invalid position");
		}
		return readCharUnsafe();
	}


	// ----------------------------------------------------------------------
	/**
	*
	*/
	void NetStreamStorage::writeChar(unsigned char value) 
	{
		store.push_back(value);
		iter_ = store.begin();
	}



	size_t NetStreamStorage::varintSize(uint_fast64_t data){
		// 7 bits -> 127
		if(data < (1LL << 7)){return 1;}
		// 14 bits -> 16383
		if(data < (1LL << 14)){return 2;}
		// 21 bits -> 2097151
		if(data < (1LL << 21)){return 3;}
		// 28 bits -> 268435455
		if(data < (1LL << 28)){return 4;}
		// 35 bits -> 34359738367
		if(data < (1LL << 35)){return 5;}
		// 42 bits -> 4398046511103
		if(data < (1LL << 42)){return 6;}
		// 49 bits -> 562949953421311
		if(data < (1LL << 49)){return 7;}
		// 56 bits -> 72057594037927935
		if(data < (1LL << 56)){return 8;}	
		return 9;
	}


	// ----------------------------------------------------------------------
	/**
	* Reads a varint form the array
	* @return The read varint 
	*/
	int_fast64_t NetStreamStorage::readVarint()	
	{
		uint_fast64_t number = readUnsignedVarint();
		return (int_fast64_t)((number & 1) == 0) ? number >> 1 : -(number >> 1);
	}
	// ----------------------------------------------------------------------
	/**
	*
	*/
	void NetStreamStorage::writeVarint(int_fast64_t value) 
	{
		writeUnsignedVarint((value << 1) ^ (value >> 63));
	}
	// ----------------------------------------------------------------------
	/**
	* Reads a unsigned varint form the array
	* @return The read u_varint 
	*/
	uint_fast64_t NetStreamStorage::readUnsignedVarint()	
	{
		// TODO
		return 0;
	}
	// ----------------------------------------------------------------------
	/**
	*
	*/
	void NetStreamStorage::writeUnsignedVarint(uint_fast64_t value) 
	{
		size_t size = varintSize(value);
		
		unsigned char buffer[size];
		for(int i = 0; i < size; i++){
			int head=128;
			if(i==size-1) head = 0;
			long b = ((value >> (7*i)) & 127) ^ head;
			buffer[size-1-i] = ((unsigned char)(b & 255 ));
		}
		writeByEndianess(buffer, size);
	}


	// ----------------------------------------------------------------------
	/**
	* Reads a byte form the array
	* @return The read byte (between -128 and 127)
	*/
	int NetStreamStorage::readByte()	
	{
		int i = static_cast<int>(readChar());
		if (i < 128) return i;
		else return (i - 256);
	}


	// ----------------------------------------------------------------------
	/**
	*
	*/
	void NetStreamStorage::writeByte(int value) 
	{
		if (value < -128 || value > 127)
		{
			throw std::invalid_argument("NetStreamStorage::writeByte(): Invalid value, not in [-128, 127]");
		}
		writeChar( static_cast<unsigned char>( (value+256) % 256 ) );
	}


	// ----------------------------------------------------------------------
	/**
	* Reads an unsigned byte form the array
	* @return The read byte (between 0 and 255)
	*/
	int NetStreamStorage::readUnsignedByte()	
	{
		return static_cast<int>(readChar());
	}


	// ----------------------------------------------------------------------
	/**
	*
	*/
	void NetStreamStorage::writeUnsignedByte(int value) 
	{
		if (value < 0 || value > 255)
		{
			throw std::invalid_argument("NetStreamStorage::writeUnsignedByte(): Invalid value, not in [0, 255]");
		}
		writeChar( static_cast<unsigned char>( value ));
	}


	// -----------------------------------------------------------------------
	/**
	* Reads a string form the array
	* @return The read string
	*/
	std::string NetStreamStorage::readString() 
	{
		int len = readInt();
		checkReadSafe(len);
		StorageType::const_iterator end = iter_;
		std::advance(end, len);
		const string tmp(iter_, end);
		iter_ = end;
		return tmp;
	}


	// ----------------------------------------------------------------------
	/**
	* Writes a string into the array;
	* @param s		The string to be written
	*/
	void NetStreamStorage::writeString(const std::string &s) 
	{
		writeUnsignedVarint(static_cast<size_t>(s.length()));
		store.insert(store.end(), s.begin(), s.end());
		iter_ = store.begin();
	}


	// -----------------------------------------------------------------------
	/**
	* Reads a string list form the array
	* @return The read string
	*/
	std::vector<std::string> NetStreamStorage::readStringList() 
	{
		std::vector<std::string> tmp;
		const int len = readInt();
		tmp.reserve(len);
		for (int i = 0; i < len; i++) 
		{
			tmp.push_back(readString());
		}
		return tmp;
	}


	// ----------------------------------------------------------------------
	/**
	* Writes a string into the array;
	* @param s		The string to be written
	*/
	void NetStreamStorage::writeStringList(const std::vector<std::string> &s) 
	{
		writeUnsignedVarint(s.size());
        for (std::vector<std::string>::const_iterator it = s.begin(); it!=s.end() ; it++) 
		{
			writeString(*it);
        }
	}


	// ----------------------------------------------------------------------
	/**
	* Restores an integer, which was split up in two bytes according to the
	* specification, it must have been split by its row byte representation
	* with MSBF-order
	*
	* @return the unspoiled integer value (between -32768 and 32767)
	*/
	int NetStreamStorage::readShort() 
	{
		short value = 0;
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		readByEndianess(p_value, 2);
		return value;
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writeShort( int value ) 
	{
		if (value < -32768 || value > 32767)
		{
			throw std::invalid_argument("NetStreamStorage::writeShort(): Invalid value, not in [-32768, 32767]");
		}

		short svalue = static_cast<short>(value);
		unsigned char *p_svalue = reinterpret_cast<unsigned char*>(&svalue);
		writeByEndianess(p_svalue, 2);
		
	}


	// ----------------------------------------------------------------------
	/**
	* restores an integer, which was split up in four bytes acording to the
	* specification, it must have been split by its row byte representation
	* with MSBF-order
	*
	* @return the unspoiled integer value (between -2.147.483.648 and 2.147.483.647)
	*/
	int NetStreamStorage::readInt() 
	{
		int value = 0;
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		readByEndianess(p_value, 4);
		return value;
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writeInt( int value ) 
	{
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		writeByEndianess(p_value, 4);
	}

	// ----------------------------------------------------------------------
	/**
	* restores a long, which was split up in height bytes acording to the
	* specification, it must have been split by its row byte representation
	* with MSBF-order
	*
	* @return the unspoiled integer value (between -??? and ???)
	*/
	long NetStreamStorage::readLong() 
	{
		long value = 0L;
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		readByEndianess(p_value, sizeof(long));
		return value;
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writeLong( long value ) 
	{
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		writeByEndianess(p_value, sizeof(long));
	}



	long long NetStreamStorage::readLongLong() 
	{
		long long value = 0L;
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		readByEndianess(p_value, sizeof(long long));
		return value;
	}
	
	void NetStreamStorage::writeLongLong( long long value ) 
	{
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		writeByEndianess(p_value, sizeof(long long));
	}	



	// ----------------------------------------------------------------------
	/**
	* restores a float , which was split up in four bytes acording to the
	* specification, it must have been split by its row byte representation
	* with MSBF-order
	*
	* @return the unspoiled float value
	*/
	float NetStreamStorage::readFloat() 
	{
		float value = 0;
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		readByEndianess(p_value, 4);
		return value;
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writeFloat( float value ) 
	{
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		writeByEndianess(p_value, 4);
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writeDouble( double value ) 
	{
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		writeByEndianess(p_value, 8);
	}


	// ----------------------------------------------------------------------
	double NetStreamStorage::readDouble( ) 
	{
		double value = 0;
		unsigned char *p_value = reinterpret_cast<unsigned char*>(&value);
		readByEndianess(p_value, 8);
		return value;
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writePacket(unsigned char* packet, int length)
	{
		store.insert(store.end(), &(packet[0]), &(packet[length]));
		iter_ = store.begin();   // reserve() invalidates iterators
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writeStorage(NetStreamStorage& other)
	{
		// the compiler cannot deduce to use a const_iterator as source
		store.insert<StorageType::const_iterator>(store.end(), other.iter_, other.store.end());
		iter_ = store.begin();
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::checkReadSafe(unsigned int num) const  
	{
		if (std::distance(iter_, store.end()) < static_cast<int>(num))
		{
			std::ostringstream msg;
			msg << "netstream::Storage::readIsSafe: want to read "  << num << " bytes from Storage, "
				<< "but only " << std::distance(iter_, store.end()) << " remaining";
			throw std::invalid_argument(msg.str());
		}
	}


	// ----------------------------------------------------------------------
	unsigned char NetStreamStorage::readCharUnsafe()
	{
		char hb = *iter_;
		++iter_;
		return hb;
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::writeByEndianess(const unsigned char * begin, unsigned int size)
	{
		const unsigned char * end = &(begin[size]);
		if (bigEndian_)
			store.insert(store.end(), begin, end);
		else
			store.insert(store.end(), std::reverse_iterator<const unsigned char *>(end), std::reverse_iterator<const unsigned char *>(begin));
		iter_ = store.begin();
	}


	// ----------------------------------------------------------------------
	void NetStreamStorage::readByEndianess(unsigned char * array, int size)
	{
		checkReadSafe(size);
		if (bigEndian_)
		{
			for (int i = 0; i < size; ++i)
				array[i] = readCharUnsafe();
		}
		else
		{
			for (int i = size - 1; i >= 0; --i)
				array[i] = readCharUnsafe();
		}
	}

  // -----------------------------------------------------------------------
  NetStreamStorage NetStreamStorage::operator+(const NetStreamStorage &storage)
  {
    NetStreamStorage msg;
    msg.store.insert(msg.store.end(), store.begin(), store.end());
    msg.store.insert(msg.store.end(), storage.begin(), storage.end());
    return msg;
  }

  // ------------------------------------------------------------------------
  
   ostream &operator<<( ostream &out, const  NetStreamStorage & s)
  {
    out<<"[";
    
    for(NetStreamStorage::StorageType::const_iterator i = s.store.begin(); i != s.store.end(); i++){
      out<<(int)(*i)<<" ";
    }
    return out<<"]"<<endl;
  }



}

/*-----------------------------------------------------------------------
 * Source  $Source: $
 * Version $Revision: 483 $
 * Date    $Date: 2010-12-21 10:42:00 +0100 (Tue, 21 Dec 2010) $
 *-----------------------------------------------------------------------
 * $Log: $
 *-----------------------------------------------------------------------*/
