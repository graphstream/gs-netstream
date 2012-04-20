/**
 *
 *
 * Copyright (c) 2010-2011 University of Luxembourg
 *
 *
 * @file netstream_constants.h
 * @date 2011-08-21
 *
 * @author Yoann Pigné
 */

#ifndef NETSTREAM_CONSTANTS_H
#define NETSTREAM_CONSTANTS_H

namespace netstream{

/** 
 *  Followed by an 32-bit signed integer for this protocol version. Certainly useless.
 */
   const unsigned char EVENT_GETVERSION=0x00;
/**
 *  Not used.
 */
   const unsigned char EVENT_START=0x01;
/** 
 *	Not used.
 */
   const unsigned char EVENT_END=0x02;


//
// ----------------------------------
//     GraphStream's graph events
// ----------------------------------
//
 	
/**
 *  Followed by a node id (TYPE_STRING format)
 */
   const unsigned char EVENT_ADD_NODE=0x10;

/**
 *  Followed by a node id (TYPE_STRING format)
 */
   const unsigned char EVENT_DEL_NODE=0x11;

/**
 * Followed by 
 *  - an edge id (TYPE_STRING format), 
 *  - an source node id (TYPE_STRING format), 
 *  - a target node id (TYPE_STRING format
 *  - a boolean indicating if directed (TYPE_BOOLEAN format) 
 */
 const unsigned char EVENT_ADD_EDGE=0x12;

/**
 * Followed by an edge id (TYPE_STRING format) 
 */
   const unsigned char EVENT_DEL_EDGE=0x13; 

/**
 * Followed by double (TYPE_DOUBLE format) 
 */
   const unsigned char EVENT_STEP=0x14;
/**
 * 
 */
   const unsigned char EVENT_CLEARED=0x15;

/**
 * Followed by 
 *  - an attribute id (TYPE_STRING format)
 *  - the attribute TYPE
 *  - the attribute value 
 */
 const unsigned char EVENT_ADD_GRAPH_ATTR=0x16;
/**
 * Followed by 
 *  - an attribute id (TYPE_STRING format)
 *  - the attribute TYPE
 *  - the attribute old value
 *  - the attribute new value 
 */
 const unsigned char EVENT_CHG_GRAPH_ATTR=0x17;
/**
 * Followed by 
 *  - the attribute id (TYPE_STRING format)
 */
 const unsigned char EVENT_DEL_GRAPH_ATTR=0x18;

/**
 * Followed by 
 *  - an attribute id (TYPE_STRING format)
 *  - the attribute TYPE
 *  - the attribute value 
 */
 const unsigned char EVENT_ADD_NODE_ATTR=0x19;
/**
 * Followed by 
 *  - an attribute id (TYPE_STRING format)
 *  - the attribute TYPE
 *  - the attribute old value
 *  - the attribute new value 
 */
 const unsigned char EVENT_CHG_NODE_ATTR=0x1a;
/**
 * Followed by 
 *  - the node id (TYPE_STRING format)
 *  - the attribute id (TYPE_STRING format)
 */
 const unsigned char EVENT_DEL_NODE_ATTR=0x1b;
/**
 * Followed by 
 *  - an attribute id (TYPE_STRING format)
 *  - the attribute TYPE
 *  - the attribute value 
 */
 const unsigned char EVENT_ADD_EDGE_ATTR=0x1c;
/**
 * Followed by 
 *  - an attribute id (TYPE_STRING format)
 *  - the attribute TYPE
 *  - the attribute old value
 *  - the attribute new value 
 */
 const unsigned char EVENT_CHG_EDGE_ATTR=0x1d;
/**
 * Followed by 
 *  - the edge id (TYPE_STRING format)
 *  - the attribute id (TYPE_STRING format)
 */
 const unsigned char EVENT_DEL_EDGE_ATTR=0x1e;




// Values types

/**
 *  Followed by a byte who's value is 0 or 1
 */
   const unsigned char TYPE_BOOLEAN=0x50;
/** 
 *  An array of booleans. Followed by first, a 16-bits integer for the number
 *  of booleans and then, a list of bytes who's value is 0 or 1
 */
 const unsigned char TYPE_BOOLEAN_ARRAY=0x51;
/**
 * Followed by a signed byte [-127,127] 
 */
   const unsigned char TYPE_BYTE=0x52;
/**
 * An array of bytes. Followed by first, a 16-bits integer for the number
 * of integers and then, a list of signed bytes.
 */
 const unsigned char TYPE_BYTE_ARRAY=0x53;
/**
 * Followed by an 16-bit signed integer (a short)
 */
   const unsigned char TYPE_SHORT=0x54;
/**
 * An array of shorts. Followed by first, a 16-bits integer for the number
 * of integers and then, a list of 16-bit signed shorts
 */
 const unsigned char TYPE_SHORT_ARRAY=0x55;
/**
 * Followed by an 32-bit signed integer
 */
   const unsigned char TYPE_INT=0x56;
/**
 * An array of integers. Followed by first, a 16-bits integer for the number
 * of integers and then, a list of 32-bit signed integers
 */
 const unsigned char TYPE_INT_ARRAY=0x57;
/**
 *  Followed by an 64-bit signed integer
 */
   const unsigned char TYPE_LONG=0x58;
/**
 * An array of longs. Followed by first, a 16-bits integer for the number of
 * longs and then, a list of 62-bit signed integers
 */
 const unsigned char TYPE_LONG_ARRAY=0x59;
/**
 *  Followed by a single precision 32-bits floating point number
 */
   const unsigned char TYPE_FLOAT=0x5a;
/**
 * Array of double. Followed by first, a 16-bits integer for the number of
 * floats and then, a list of 32-bit floats
 */
 const unsigned char TYPE_FLOAT_ARRAY=0x5b;
/**
 *  Followed by a double precision 64-bits floating point number
 */
   const unsigned char TYPE_DOUBLE=0x5c;
/**
 * Array of double. Followed by first, a 16-bits integer for the number of
 * doubles and then, a list of 64-bit doubles
 */
 const unsigned char TYPE_DOUBLE_ARRAY=0x5d;
/**
 * Array of characters. Followed by first, a 16-bits integer for the size in
 * bytes (not in number of characters) of the string, then by the unicode
 * string
 */
 const unsigned char TYPE_STRING=0x5e;
/**
 * Raw data, good for serialization. Followed by first, a 16-bits integer
 * indicating the length in bytes of the dataset, and then the data itself.
 */
 const unsigned char TYPE_RAW=0x5f;

/**
 * An type-unspecified array. Followed by first, a
 * 16-bits integer indicating the number of elements, and then, the elements
 * themselves. The elements themselves have to give their type.
 */
 const unsigned char TYPE_ARRAY=0x60;

}// end netstream namespace

#endif
