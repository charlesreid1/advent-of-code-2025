CC = gcc
CFLAGS = -Wall -Wextra -O2

all: round1 round2 round2_tree_final

round1: round1.c
	$(CC) $(CFLAGS) -o round1 round1.c

round2: round2.c
	$(CC) $(CFLAGS) -o round2 round2.c

round2_tree_final: round2_tree_final.c
	$(CC) $(CFLAGS) -o round2_tree_final round2_tree_final.c

clean:
	rm -f round1 round2 round2_tree_final

test: round1 round2 round2_tree_final
	@echo "Testing round1:"
	@./round1 ../example
	@echo "Testing round2:"
	@./round2 ../example
	@echo "Testing round2_tree_final:"
	@./round2_tree_final ../example

.PHONY: all clean test