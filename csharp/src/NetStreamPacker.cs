namespace Netstream
{
    public abstract class NetStreamPacker
    {
        /**
         * Pack the given ByteBuffer from startIndex to endIdex 
         * @param buffer The buffer to pack/encode
         * @param startIndex the index at which the encoding starts in the buffer
         * @param endIndex the index at which the encoding stops
         * @return a ByteBuffer that is the packed version of the input one. It may not have the same size.
         */
        public abstract NetStreamStorage PackMessage(NetStreamStorage buffer, int startIndex, int endIndex);

        /**
         * Pack the given ByteBuffer form its position to its capacity.
         * @param buffer The buffer to pack/encode
         * @return a ByteBuffer that is the packed version of the input one. It may not have the same size.
         */
        public NetStreamStorage PackMessage(NetStreamStorage buffer)
        {
            return this.PackMessage(buffer, 0, buffer.Capacity);
        }

        /**
         * @param capacity
         * @return
         */
        public abstract NetStreamStorage PackMessageSize(int capacity);
    }
}
