from pathlib import Path
from collections import defaultdict

def part1(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    grid = []
    start_col = -1
    
    try:
        with open(f, 'r') as file:
            for r_idx, line in enumerate(file):
                line = line.strip()
                if not line:
                    continue
                grid.append(list(line))
                if 'S' in line:
                    start_row = r_idx
                    start_col_s = line.find('S')
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return

    if not grid or start_row == -1:
        print("Error: Could not parse grid or find starting point 'S'")
        return

    rows = len(grid)
    cols = len(grid[0])

    split_count = 0
    
    # Active beams are represented by their column indices
    active_beams = {start_col_s}

    # Simulate beams moving downwards
    for r in range(start_row + 1, rows): # Start from the row below 'S'
        if not active_beams:
            break # No more active beams
            
        next_active_beams = set()
        
        for c in active_beams:
            if not (0 <= c < cols): # Beam went off grid horizontally
                continue

            current_char = grid[r][c]

            if current_char == '^':
                split_count += 1
                # New beams to the left and right
                if c - 1 >= 0:
                    next_active_beams.add(c - 1)
                if c + 1 < cols:
                    next_active_beams.add(c + 1)
            elif current_char == '.':
                # Beam continues downwards
                next_active_beams.add(c)
            # If it's 'S', we already processed it as starting point, it won't be a splitter or empty space in later rows
            # Any other character (e.g., if input had an invalid char) would stop the beam
        
        active_beams = next_active_beams
            
    print(split_count)

def part2(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    grid = []
    start_row = -1
    start_col = -1
    
    try:
        with open(f, 'r') as file:
            for r_idx, line in enumerate(file):
                line = line.strip()
                if not line:
                    continue
                grid.append(list(line))
                if 'S' in line:
                    start_row = r_idx
                    start_col = line.find('S')
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return

    if not grid or start_row == -1:
        print("Error: Could not parse grid or find starting point 'S'")
        return

    rows = len(grid)
    cols = len(grid[0])
    
    total_completed_timelines = 0
    # timelines: dict mapping column index to number of timelines at that position for the current row
    timelines = {start_col: 1}

    # Simulate particle moving downwards row by row
    for r in range(start_row, rows):
        next_timelines = defaultdict(int)
        
        for c, count in timelines.items():
            if not (0 <= c < cols):
                # This timeline went off the side on the previous step, so it's completed.
                total_completed_timelines += count
                continue

            current_char = grid[r][c]

            if current_char == 'S' or current_char == '.':
                # Particle continues downwards
                next_timelines[c] += count
            elif current_char == '^':
                # Time splits, particle goes left and right
                next_timelines[c - 1] += count
                next_timelines[c + 1] += count
        
        timelines = next_timelines
            
    # Any timelines remaining in the `timelines` dict have exited the bottom of the grid.
    total_completed_timelines += sum(timelines.values())
    
    print(total_completed_timelines)

if __name__ == "__main__":
    part1('example')
    part1('input')
    part2('example')
    part2('input')