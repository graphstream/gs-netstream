BINDIR=bin
OBJDIR=obj
SRCDIR=src
INCDIR=include

CC = g++
CWARN = -W -Wall -Wshadow -Wimplicit -Wreturn-type -Wcomment -Wtrigraphs -Wformat -Wparentheses -Wpointer-arith -Wuninitialized -O

CDBG = -g $(CWARN) -fno-inline
CFLAGS = -I$(INCDIR) $(CDBG)
DFLAGS = -I$(INCDIR) -g $(CWARN) -fno-inline -DDEBUG=1

CTAG = ctags
CTAGFILE = filelist
# src, object and bin files
MAIN := netstream-main 

HEADERS = $(INCDIR)/global.h

OBJS = \
    $(OBJDIR)/tcpip/storage.o  \
	$(OBJDIR)/tcpip/socket.o \
    $(OBJDIR)/netstream-sender.o \
	$(OBJDIR)/netstream-main.o 
	 
.SECONDARY:

#-- Rules
all : $(MAIN)

$(MAIN) : $(OBJS)
	$(CC) $(CFLAGS) $(OBJS)  -o $(MAIN)
	
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
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
	-rm -f $(MAIN)

fresh : clean all