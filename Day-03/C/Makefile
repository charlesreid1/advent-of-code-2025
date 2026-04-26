# Makefile for Day 3: Lobby - Obfuscated C Solution
# IOCCC-style obfuscated program for Advent of Code 2025 Day 3

CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11
TARGET = solution

all: $(TARGET)

$(TARGET): solution.c
	$(CC) $(CFLAGS) -o $(TARGET) solution.c

test: $(TARGET)
	@echo "=== Testing with example input ==="
	@./$(TARGET) < ../../example
	@echo ""
	@echo "=== Testing with full input ==="
	@./$(TARGET) < ../../input

clean:
	rm -f $(TARGET)

.PHONY: all test clean