CC = gcc
CFLAGS = -Wall -Wextra -O2

all: solution

solution: solution.c
	$(CC) $(CFLAGS) -o solution solution.c

clean:
	rm -f solution

test: solution
	@echo "Testing solution:"
	@./solution ../example

.PHONY: all clean test
