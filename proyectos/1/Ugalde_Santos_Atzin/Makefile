CC := gcc
CFLAGS := -Wall -Wextra -Wpedantic -funsigned-char -std=c99
RM := rm -rf

.PHONY: all

all: fiunamfs

fiunamfs: src/main.c src/fs.c src/ls.c src/error.c src/misc.c src/rm.c src/cp.c
	$(CC) $(CFLAGS) src/main.c src/fs.c src/ls.c src/error.c src/misc.c src/rm.c src/cp.c -o fiunamfs

clean:
	$(RM) fiunamfs
