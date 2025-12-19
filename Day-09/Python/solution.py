from pathlib import Path
from collections import deque

def part1(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    red_tiles = []
    try:
        with open(f, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    x, y = map(int, line.split(','))
                    red_tiles.append((x, y))
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return
    except ValueError:
        print(f"Error: Invalid coordinate format in '{filename}'")
        return

    max_area = 0
    num_red_tiles = len(red_tiles)
    for i in range(num_red_tiles):
        for j in range(i + 1, num_red_tiles):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            if width > 0 and height > 0:
                area = width * height
                if area > max_area:
                    max_area = area
    
    print(max_area)

def part2(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    red_tiles = []
    try:
        with open(f, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    x, y = map(int, line.split(','))
                    red_tiles.append((x, y))
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return
    except ValueError:
        print(f"Error: Invalid coordinate format in '{filename}'")
        return

    if not red_tiles:
        print(0)
        return

    # --- 1. Coordinate Compression with Margin ---
    x_coords = list(set(p[0] for p in red_tiles))
    y_coords = list(set(p[1] for p in red_tiles))
    
    all_x = sorted(list(set(x_coords + [min(x_coords) - 1, max(x_coords) + 1])))
    all_y = sorted(list(set(y_coords + [min(y_coords) - 1, max(y_coords) + 1])))

    map_x = {x: i for i, x in enumerate(all_x)}
    map_y = {y: i for i, y in enumerate(all_y)}

    nx, ny = len(all_x), len(all_y)

    # --- 2. Mark Polygon Boundaries on Compressed Grid ---
    h_walls = [[False] * ny for _ in range(nx - 1)]
    v_walls = [[False] * (ny - 1) for _ in range(nx)]

    num_red_tiles = len(red_tiles)
    for i in range(num_red_tiles):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % num_red_tiles]

        if y1 == y2:  # Horizontal segment
            ix1, ix2 = map_x[min(x1, x2)], map_x[max(x1, x2)]
            if y1 in map_y:
                iy = map_y[y1]
                for ix in range(ix1, ix2):
                    h_walls[ix][iy] = True
        else:  # Vertical segment
            iy1, iy2 = map_y[min(y1, y2)], map_y[max(y1, y2)]
            if x1 in map_x:
                ix = map_x[x1]
                for iy in range(iy1, iy2):
                    v_walls[ix][iy] = True

    # --- 3. Flood Fill to Find Exterior Cells ---
    exterior_cells = set()
    q = deque([(0, 0)])
    visited = set([(0, 0)])

    while q:
        cx, cy = q.popleft()
        exterior_cells.add((cx, cy))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx_cell, ny_cell = cx + dx, cy + dy

            if not (0 <= nx_cell < nx - 1 and 0 <= ny_cell < ny - 1):
                continue
            if (nx_cell, ny_cell) in visited:
                continue

            # Check for walls between (cx,cy) and (nx_cell, ny_cell)
            wall_found = False
            if dx == 1: wall_found = v_walls[cx + 1][cy]
            elif dx == -1: wall_found = v_walls[cx][cy]
            elif dy == 1: wall_found = h_walls[cx][cy + 1]
            elif dy == -1: wall_found = h_walls[cx][cy]
            
            if not wall_found:
                visited.add((nx_cell, ny_cell))
                q.append((nx_cell, ny_cell))
    
    # --- 4. Build Summed-Area Table (SAT) ---
    sat = [[0] * ny for _ in range(nx)]
    for i in range(nx - 1):
        for j in range(ny - 1):
            is_exterior = 1 if (i, j) in exterior_cells else 0
            sat[i + 1][j + 1] = is_exterior + sat[i][j + 1] + sat[i + 1][j] - sat[i][j]

    def query_sat(r1, c1, r2, c2):
        if r1 >= r2 or c1 >= c2: return 0
        return sat[r2][c2] - sat[r1][c2] - sat[r2][c1] + sat[r1][c1]

    # --- 5. Check all Red Tile Pairs ---
    max_area = 0
    for i in range(num_red_tiles):
        for j in range(i + 1, num_red_tiles):
            p1_x, p1_y = red_tiles[i]
            p2_x, p2_y = red_tiles[j]

            rect_x1, rect_x2 = min(p1_x, p2_x), max(p1_x, p2_x)
            rect_y1, rect_y2 = min(p1_y, p2_y), max(p1_y, p2_y)

            comp_x1, comp_x2 = map_x[rect_x1], map_x[rect_x2]
            comp_y1, comp_y2 = map_y[rect_y1], map_y[rect_y2]

            if query_sat(comp_x1, comp_y1, comp_x2, comp_y2) == 0:
                area = (rect_x2 - rect_x1 + 1) * (rect_y2 - rect_y1 + 1)
                if area > max_area:
                    max_area = area
    
    print(max_area)


if __name__ == "__main__":
    part1('example')
    part1('input')
    part2('example')
    part2('input')