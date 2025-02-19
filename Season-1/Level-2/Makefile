CC = gcc
CFLAGS = -Wall -Wextra -g
SRC = code.c tests.c hack.c
OBJS = $(SRC:.c=.o)

all: tests hack

tests: code.c tests.c
	$(CC) $(CFLAGS) -o tests tests.c code.c

hack: code.c hack.c
	$(CC) $(CFLAGS) -o hack hack.c code.c

clean:
	rm -f tests hack
