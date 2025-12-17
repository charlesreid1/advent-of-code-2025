import sys
import os

def part1(filename):
    current_position = 50
    zero_count = 0

    f = os.path.join('..', filename)
    try:
        with open(f, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                direction = line[0]
                distance = int(line[1:])

                if direction == 'R':
                    current_position = (current_position + distance) % 100
                elif direction == 'L':
                    current_position = (current_position - distance) % 100
                
                if current_position == 0:
                    zero_count += 1
        
        print(zero_count)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

def part2(filename):
    # current_position_unwrapped tracks the dial's position as if it were on an infinite number line,
    # allowing us to correctly count passes through 0 (or multiples of 100).
    current_position_unwrapped = 50
    zero_count = 0

    f = os.path.join('..', filename)
    try:
        with open(f, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                direction = line[0]
                distance = int(line[1:])

                if direction == 'R':
                    # We are counting how many multiples of 100 are crossed when moving right.
                    # We are counting how many '0's are hit in the range
                    # (current_position_unwrapped, current_position_unwrapped + distance].
                    # The number of such multiples is floor(B/100) - floor(A/100) for range (A, B].
                    zero_count += (current_position_unwrapped + distance) // 100 - current_position_unwrapped // 100
                    current_position_unwrapped += distance
                elif direction == 'L':
                    # We are counting how many multiples of 100 are crossed when moving left.
                    # We are counting how many '0's are hit in the range
                    # [current_position_unwrapped - distance, current_position_unwrapped).
                    # The number of such multiples is (B-1)//100 - (A-1)//100 for range [A, B).
                    zero_count += (current_position_unwrapped - 1) // 100 - (current_position_unwrapped - distance - 1) // 100
                    current_position_unwrapped -= distance
        
        print(zero_count)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    part1("example")
    part1("input")
    part2("example")
    part2("input")

