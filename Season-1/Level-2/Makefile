CC = gcc
CFLAGS = -Wall -Wextra -g
SRC = code.c tests.c hack.c
OBJS = $(SRC:.c=.o)

# The default target is to build both tests and hack executables
all: tests hack

# Rule to build the tests executable
tests: code.o tests.o
	$(CC) $(CFLAGS) -o tests tests.o code.o

# Rule to build the hack executable
hack: code.o hack.o
	$(CC) $(CFLAGS) -o hack hack.o code.o

# Rule to compile code.c into code.o
code.o: code.c code.h
	$(CC) $(CFLAGS) -c code.c

# Rule to compile tests.c into tests.o
tests.o: tests.c code.h
	$(CC) $(CFLAGS) -c tests.c

# Rule to compile hack.c into hack.o
hack.o: hack.c code.h
	$(CC) $(CFLAGS) -c hack.c

# Clean up object files and executables
clean:
	rm -f *.o tests hack
