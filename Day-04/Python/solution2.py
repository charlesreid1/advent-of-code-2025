def part2(filename):
    with open(filename, 'r') as f:
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
    part2("input")
