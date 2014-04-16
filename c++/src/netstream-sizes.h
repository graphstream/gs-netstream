/**
 *
 *
 * @file netstream-sizes.h
 * @date 2011-08-21
 *
 * @author Adrian Pop
 *
 * define sizes for different platforms
 */

#ifndef NETSTREAM_SIZES_H
#define NETSTREAM_SIZES_H

#if defined(__MINGW32__)
#include <stdint.h>
#include <windows.h>
#define sleep Sleep
#endif


using namespace std;

namespace netstream{

#define GS_CHAR    char
#define GS_BOOL    bool
#define GS_INT     int
#if defined(__MINGW32__)
#define GS_LONG    int64_t
#else
#define GS_LONG    long
#endif
#define GS_FLOAT   float
#define GS_DOUBLE  double
#define GS_STRING  string

}// end netstream namespace

#endif
