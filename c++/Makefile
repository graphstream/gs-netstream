BINDIR=bin
OBJDIR=obj
SRCDIR=src
INCDIR=include

CC = g++
CWARN = -W -Wall -Wshadow -Wimplicit -Wreturn-type -Wcomment -Wtrigraphs -Wformat -Wparentheses -Wpointer-arith -Wuninitialized -O

CDBG = -g $(CWARN) -fno-inline
CFLAGS = -I$(INCDIR) -O3 
DFLAGS = -I$(INCDIR) -g $(CWARN) -fno-inline -DDEBUG=1

CTAG = ctags
CTAGFILE = filelist
# src, object and bin files
OUT_BINARY := netstream-main 
OUT_LIBRARY := libnetstream.a

HEADERS = $(INCDIR)/global.h

OBJS = \
    $(OBJDIR)/netstream-storage.o  \
	$(OBJDIR)/netstream-socket.o \
    $(OBJDIR)/netstream-sender.o \
	$(OBJDIR)/netstream-main.o 
	 
.SECONDARY:

#-- Rules
all : $(OUT_BINARY) $(OUT_LIBRARY)

$(OUT_BINARY) : $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(OUT_BINARY)

$(OUT_LIBRARY) : $(OBJS)
	libtool -static -o $(OUT_LIBRARY)  $(OBJS)

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c $? -o $@ 

.PHONY : clean depend fresh

tag :
	find src/*.cpp include/*.h > filelist
	$(CTAG) -L $(CTAGFILE)

clean :
	-rm -f $(OBJDIR)/*.o $(PARSE_C) $(PARSE_H)
	-rm -f $(OBJDIR)/*/*.o $(PARSE_C) $(PARSE_H)
	-rm -f $(SRCDIR)/*.output $(LEX_C)
	-rm -f */*~ *~ core
	-rm -f $(BINDIR)/*
	-rm -f $(OUT_BINARY)
	-rm -f $(OUT_LIBRARY)

fresh : clean all
