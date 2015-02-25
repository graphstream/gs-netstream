namespace Netstream
{
    //
    // ----------------------------------
    // GraphStream's graph events
    // ----------------------------------
    //

    public enum NetStreamEvent
    { 
        /**
         * Followed by a node id (TYPE_STRING format)
         */
        AddNode = 0x10,

        /**
         * Followed by a node id (TYPE_STRING format)
         */
        DelNode = 0x11,

        /**
         * Followed by - an edge id (TYPE_STRING format), - an source node id
         * (TYPE_STRING format), - a target node id (TYPE_STRING format - a boolean
         * indicating if directed (TYPE_BOOLEAN format)
         */
        AddEdge = 0x12,

        /**
         * Followed by an edge id (TYPE_STRING format)
         */
        DelEdge = 0x13,

        /**
         * Followed by double (TYPE_DOUBLE format)
         */
        Step = 0x14,

        /**
         * 
         */
        Cleared = 0x15,

        /**
         * Followed by - an attribute id (TYPE_STRING format) - the attribute TYPE -
         * the attribute value
         */
        AddGraphAttr = 0x16,

        /**
         * Followed by - an attribute id (TYPE_STRING format) - the attribute TYPE -
         * the attribute old value - the attribute new value
         */
        ChgGraphAttr = 0x17,

        /**
         * Followed by - the attribute id (TYPE_STRING format)
         */
        DelGraphAttr = 0x18,

        /**
         * Followed by - an attribute id (TYPE_STRING format) - the attribute TYPE -
         * the attribute value
         */
        AddNodeAttr = 0x19,

        /**
         * Followed by - an attribute id (TYPE_STRING format) - the attribute TYPE -
         * the attribute old value - the attribute new value
         */
        ChgNodeAttr = 0x1a,

        /**
         * Followed by - the node id (TYPE_STRING format) - the attribute id
         * (TYPE_STRING format)
         */
        DelNodeAttr = 0x1b,

        /**
         * Followed by - an attribute id (TYPE_STRING format) - the attribute TYPE -
         * the attribute value
         */
        AddEdgeAttr = 0x1c,

        /**
         * Followed by - an attribute id (TYPE_STRING format) - the attribute TYPE -
         * the attribute old value - the attribute new value
         */
        ChgEdgeAttr = 0x1d,

        /**
         * Followed by - the edge id (TYPE_STRING format) - the attribute id
         * (TYPE_STRING format)
         */
        DelEdgeAttr = 0x1e
    }

    // Values types

    public enum NetStreamType
    {
        /**
         * Followed by a byte who's value is 0 or 1
         */
        Boolean = 0x50,

        /**
         * An array of booleans. Followed by first, a 16-bits integer for the number
         * of booleans and then, a list of bytes who's value is 0 or 1
         */
        BooleanArray = 0x51,

        /**
         * Followed by a signed byte [-127,127]
         */
        Byte = 0x52,

        /**
         * An array of bytes. Followed by first, a 16-bits integer for the number of
         * integers and then, a list of signed bytes.
         */
        ByteArray = 0x53,

        /**
         * Followed by an 16-bit signed integer (a short)
         */
        Short = 0x54,

        /**
         * An array of shorts. Followed by first, a 16-bits integer for the number
         * of integers and then, a list of 16-bit signed shorts
         */
        ShortArray = 0x55,

        /**
         * Followed by an 32-bit signed integer
         */
        Int = 0x56,

        /**
         * An array of integers. Followed by first, a 16-bits integer for the number
         * of integers and then, a list of 32-bit signed integers
         */
        IntArray = 0x57,

        /**
         * Followed by an 64-bit signed integer
         */
        Long = 0x58,

        /**
         * An array of longs. Followed by first, a 16-bits integer for the number of
         * longs and then, a list of 62-bit signed integers
         */
        LongArray = 0x59,

        /**
         * Followed by a single precision 32-bits floating point number
         */
        Float = 0x5a,

        /**
         * Array of double. Followed by first, a 16-bits integer for the number of
         * floats and then, a list of 32-bit floats
         */
        FloatArray = 0x5b,

        /**
         * Followed by a double precision 64-bits floating point number
         */
        Double = 0x5c,

        /**
         * Array of double. Followed by first, a 16-bits integer for the number of
         * doubles and then, a list of 64-bit doubles
         */
        DoubleArray = 0x5d,

        /**
         * Array of characters. Followed by first, a 16-bits integer for the size in
         * bytes (not in number of characters) of the string, then by the unicode
         * string
         */
        String = 0x5e,

        /**
         * Raw data, good for serialization. Followed by first, a 16-bits integer
         * indicating the length in bytes of the dataset, and then the data itself.
         */
        Raw = 0x5f,

        /**
         * An type-unspecified array. Followed by first, a 16-bits integer
         * indicating the number of elements, and then, the elements themselves. The
         * elements themselves have to give their type.
         */
        Array = 0x60,

        /**
         * 
         */
        Null = 0x61
    }
}
