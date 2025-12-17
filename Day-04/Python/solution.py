def part1(filename):
    with open(filename, 'r') as f:
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

if __name__ == "__main__":
    part1("example")
