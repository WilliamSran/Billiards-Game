CC = clang
CFLAGS = -Wall -std=c99 -pedantic
IncPath = /usr/include/python3.11
LibPath = /usr/lib/python3.11

all:	Himo _phylib.so 

clean:
	rm -f *.o *.so *.exe *.svg

Himo:	phylib.o phylib.so
	$(CC) phylib.o -L. -Lphylib -shared -o Himo -lm 

phylib.so:	phylib.o
	$(CC) -shared -o libphylib.so phylib.o

phylib.o:	phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o
	
phylib_wrap.c:	phylib.i 
	swig -python phylib.i

phylib_wrap.o:	phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -fPIC -I$(IncPath) -o phylib_wrap.o

_phylib.so:	phylib_wrap.o phylib.so
	$(CC) $(CFLAGS) -fPIC -shared phylib_wrap.o -L. -L$(LibPath) -lpython3.11 -lphylib -o _phylib.so
