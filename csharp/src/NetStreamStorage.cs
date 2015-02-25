using System;
using System.IO;
using System.Text;

namespace Netstream
{
    public class NetStreamStorage : MemoryStream
    {
        public NetStreamStorage()
        {
        }

        public NetStreamStorage(int capacity)
            : base(capacity)
        {
        }

        public void Flip()
        {
            int position = (int) Position;
            Position = 0;
            Capacity = position;
        }

        protected NetStreamType GetNetStreamType(object value)
        {
            if (value == null)
                return NetStreamType.Null;

            Type type = value.GetType();
            bool isArray = type.IsArray;
            if (isArray)
                type = type.GetElementType();

            if (type == typeof (bool))
                return isArray ? NetStreamType.BooleanArray : NetStreamType.Boolean;
            if (type == typeof (byte) || type == typeof (char))
                return isArray ? NetStreamType.ByteArray : NetStreamType.Byte;
            if (type == typeof (short))
                return isArray ? NetStreamType.ShortArray : NetStreamType.Short;
            if (type == typeof (int))
                return isArray ? NetStreamType.IntArray : NetStreamType.Int;
            if (type == typeof (long))
                return isArray ? NetStreamType.LongArray : NetStreamType.Long;
            if (type == typeof (float))
                return isArray ? NetStreamType.FloatArray : NetStreamType.Float;
            if (type == typeof (double))
                return isArray ? NetStreamType.DoubleArray : NetStreamType.Double;
            if (type == typeof (string))
                return isArray ? NetStreamType.Array : NetStreamType.String;

            return 0;
        }

        public NetStreamStorage EncodeValueWithType(object input)
        {
            // First encode value type:
            NetStreamType valueType = GetNetStreamType(input);
            EncodeType(valueType);

            // Second encode data:
            switch (valueType)
            {
                case NetStreamType.Boolean:
                case NetStreamType.Byte:
                case NetStreamType.Short:
                case NetStreamType.Int:
                case NetStreamType.Long:
                case NetStreamType.Float:
                case NetStreamType.Double:
                    return EncodeNative(input);

                case NetStreamType.String:
                    return EncodeString((string) input);

                case NetStreamType.BooleanArray:
                case NetStreamType.ByteArray:
                case NetStreamType.ShortArray:
                case NetStreamType.IntArray:
                case NetStreamType.LongArray:
                case NetStreamType.FloatArray:
                case NetStreamType.DoubleArray:
                case NetStreamType.Array:
                    return EncodeArray((Array) input);

                case NetStreamType.Null:
                    return this;

                default:
                    return null;
            }
        }

        /**
	     * @param input
	     * @return
	     */

        public NetStreamStorage EncodeArray(Array data)
        {
            Serialize((uint)data.Length);
            foreach (object t in data)
                Serialize(t);
            return this;
        }

        /**
         * @param input
         * @return
         */

        public NetStreamStorage EncodeString(string input)
        {
            byte[] data = Encoding.UTF8.GetBytes(input);
            return EncodeArray(data);
        }

        /**
         * @param input
         * @return MemoryStream with encoded struct in it
         */

        public NetStreamStorage EncodeEvent(NetStreamEvent input)
        {
            return EncodeNative((byte) input);
        }

        /**
         * @param input
         * @return MemoryStream with encoded struct in it
         */

        public NetStreamStorage EncodeType(NetStreamType input)
        {
            return EncodeNative((byte) input);
        }

        /**
         * @param input
         * @return MemoryStream with encoded struct in it
         */

        public NetStreamStorage EncodeNative(object input)
        {
            Serialize(input);
            return this;
        }

        private byte[] GetVarint(long input)
        {
            return GetUnsignedVarint(input >= 0 ? (input << 1) : ((Math.Abs(input) << 1) ^ 1));
        }

        private byte[] GetUnsignedVarint(long number)
        {
            int byteSize = varintSize(number);
            byte[] bytes = new byte[byteSize];
            for (int i = 0; i < byteSize; i++)
            {
                int head = 128;
                if (i == byteSize - 1) head = 0;
                long b = ((number >> (7 * i)) & 127) ^ head;
                bytes[i] = (byte)(b & 255);
            }
            return bytes;
        }

        private int varintSize(long data)
        {
            // 7 bits -> 127
            if (data < (1L << 7))
            {
                return 1;
            }

            // 14 bits -> 16383
            if (data < (1L << 14))
            {
                return 2;
            }

            // 21 bits -> 2097151
            if (data < (1L << 21))
            {
                return 3;
            }

            // 28 bits -> 268435455
            if (data < (1L << 28))
            {
                return 4;
            }

            // 35 bits -> 34359738367
            if (data < (1L << 35))
            {
                return 5;
            }

            // 42 bits -> 4398046511103
            if (data < (1L << 42))
            {
                return 6;
            }

            // 49 bits -> 562949953421311
            if (data < (1L << 49))
            {
                return 7;
            }

            // 56 bits -> 72057594037927935
            if (data < (1L << 56))
            {
                return 8;
            }

            return 9;
        }

        private void Serialize(object input)
        {
            byte[] bytes;

            if (input is bool)
                bytes = BitConverter.GetBytes((bool) input);
            else if (input is byte || input is char)
                bytes = new byte[] { Convert.ToByte(input) };
            else if (input is short || input is int || input is long)
                bytes = GetVarint(Convert.ToInt64(input));
            else if (input is ushort || input is uint || input is ulong)
                bytes = GetUnsignedVarint(Convert.ToInt64(input));
            else if (input is float)
                bytes = BitConverter.GetBytes((float) input);
            else if (input is double)
                bytes = BitConverter.GetBytes((double) input);
            else
                throw new ArgumentException();

            if (BitConverter.IsLittleEndian)
                Array.Reverse(bytes);
            Write(bytes, 0, bytes.Length);
        }
    }
}
