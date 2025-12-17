from pathlib import Path


def part1(filename):
    f = Path(__file__).resolve().parent.parent / filename
    with open(f, 'r') as f:
        grid_lines = [line.strip() for line in f]

    grid = []
    for line in grid_lines:
        row = []
        for char in line:
            row.append(char)
        grid.append(row)

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    accessible_rolls = 0
    
    # Define directions for 8 neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                adjacent_rolls_count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc

                    # Check if neighbor is within grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            adjacent_rolls_count += 1
                
                if adjacent_rolls_count < 4:
                    accessible_rolls += 1
    
    print(accessible_rolls)


def part2(filename):
    f = Path(__file__).resolve().parent.parent / filename
    with open(f, 'r') as f:
        # Read lines and strip trailing newlines
        grid_lines = [line.rstrip('\n') for line in f]

    # 1. Normalize the Grid: Find the maximum width
    if not grid_lines:
        return
    
    max_cols = max(len(line) for line in grid_lines)
    
    grid = []
    for line in grid_lines:
        row = list(line)
        # 2. Pad shorter rows with '.' so the grid is a perfect rectangle
        while len(row) < max_cols:
            row.append('.')
        grid.append(row)

    rows = len(grid)
    cols = max_cols
    
    total_removed = 0
    
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    while True:
        rolls_to_remove = []
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    adjacent_rolls_count = 0
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc

                        # Check if neighbor is within grid boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Because we padded the grid, this index is now safe
                            if grid[nr][nc] == '@':
                                adjacent_rolls_count += 1
                    
                    if adjacent_rolls_count < 4:
                        rolls_to_remove.append((r, c))
        
        if not rolls_to_remove:
            break
        
        total_removed += len(rolls_to_remove)
        for r, c in rolls_to_remove:
            grid[r][c] = '.' 
            
    print(total_removed)


if __name__ == "__main__":
    part1("example")
    part1("input")
    part2("example")
    part2("input")
