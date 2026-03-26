#!/usr/bin/env python3
import sys
import time


def parse_input(data):
    lines = data.strip().split('\n')
    shapes = {}
    regions = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ':' in line:
            before_colon = line.split(':')[0].strip()
            if before_colon.isdigit():
                shape_id = int(before_colon)
                coords = set()
                i += 1
                r = 0
                while i < len(lines) and lines[i].strip():
                    row = lines[i]
                    if ':' in row:
                        break
                    for c, ch in enumerate(row):
                        if ch == '#':
                            coords.add((r, c))
                    r += 1
                    i += 1
                shapes[shape_id] = coords
                continue
            elif 'x' in before_colon:
                parts = line.split(':', 1)
                w, h = map(int, parts[0].strip().split('x'))
                counts = list(map(int, parts[1].strip().split()))
                regions.append((w, h, counts))
        i += 1
    return shapes, regions


def get_orientations(shape):
    results = set()
    coords = list(shape)
    for flip in [False, True]:
        working = [(-r, c) for r, c in coords] if flip else list(coords)
        for _ in range(4):
            min_r = min(r for r, c in working)
            min_c = min(c for r, c in working)
            norm = frozenset((r - min_r, c - min_c) for r, c in working)
            results.add(norm)
            working = [(c, -r) for r, c in working]
    return results


def greedy_solve(width, height, counts, shape_orients, num_shapes):
    """Deterministic scan-line greedy: for each empty cell, try to place a piece."""
    grid = bytearray(width * height)
    remaining = list(counts)
    total = sum(remaining)

    # Precompute index offsets for each shape's orientations
    shape_orient_data = []
    for si in range(num_shapes):
        orient_data = []
        for orient in shape_orients[si]:
            offsets = sorted(orient)
            max_dr = max(r for r, c in offsets)
            max_dc = max(c for r, c in offsets)
            idx_offsets = tuple(dr * width + dc for dr, dc in offsets)
            orient_data.append((max_dr, max_dc, idx_offsets))
        shape_orient_data.append(orient_data)

    for cell in range(width * height):
        if total == 0:
            break
        if grid[cell]:
            continue
        r, c = divmod(cell, width)
        for si in range(num_shapes):
            if remaining[si] == 0:
                continue
            placed = False
            for max_dr, max_dc, idx_offsets in shape_orient_data[si]:
                if r + max_dr >= height or c + max_dc >= width:
                    continue
                ok = True
                for off in idx_offsets:
                    if grid[cell + off]:
                        ok = False
                        break
                if ok:
                    for off in idx_offsets:
                        grid[cell + off] = 1
                    remaining[si] -= 1
                    total -= 1
                    placed = True
                    break
            if placed:
                break

    return total == 0


def backtrack_solve(width, height, counts, shape_orients, shape_areas, num_shapes):
    """Cell-by-cell backtracking with bitmask grid."""
    grid_area = width * height
    total_area = sum(counts[i] * shape_areas[i] for i in range(num_shapes))

    # Precompute placement masks indexed by min cell
    min_cell_masks = [[] for _ in range(grid_area)]
    for si in range(num_shapes):
        if counts[si] == 0:
            continue
        seen = set()
        for orient in shape_orients[si]:
            max_dr = max(r for r, c in orient)
            max_dc = max(c for r, c in orient)
            for sr in range(height - max_dr):
                for sc in range(width - max_dc):
                    mask = 0
                    mn = grid_area
                    for dr, dc in orient:
                        idx = (sr + dr) * width + (sc + dc)
                        mask |= 1 << idx
                        if idx < mn:
                            mn = idx
                    if mask not in seen:
                        seen.add(mask)
                        min_cell_masks[mn].append((si, mask, shape_areas[si]))

    full = (1 << grid_area) - 1
    remaining = list(counts)
    area_left = total_area

    def backtrack(grid, empty_left):
        nonlocal area_left
        if area_left == 0:
            return True
        if empty_left < area_left:
            return False

        avail = full & ~grid
        if not avail:
            return False
        cell = (avail & -avail).bit_length() - 1

        for si, mask, area in min_cell_masks[cell]:
            if remaining[si] <= 0 or grid & mask:
                continue
            remaining[si] -= 1
            area_left -= area
            if backtrack(grid | mask, empty_left - area):
                remaining[si] += 1
                area_left += area
                return True
            remaining[si] += 1
            area_left += area

        # Try gap
        if empty_left - 1 >= area_left:
            return backtrack(grid | (1 << cell), empty_left - 1)

        return False

    return backtrack(0, grid_area)


def solve_region(width, height, counts, shape_orients, shape_areas, num_shapes):
    total_area = sum(counts[i] * shape_areas[i] for i in range(num_shapes))
    grid_area = width * height
    if total_area > grid_area:
        return False
    if sum(counts) == 0:
        return True

    if greedy_solve(width, height, counts, shape_orients, num_shapes):
        return True

    return backtrack_solve(width, height, counts, shape_orients, shape_areas, num_shapes)


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    shapes, regions = parse_input(data)
    num_shapes = len(shapes)
    shape_areas = {i: len(s) for i, s in shapes.items()}
    shape_orients = {i: list(get_orientations(s)) for i, s in shapes.items()}

    result = 0
    for w, h, counts in regions:
        if solve_region(w, h, counts, shape_orients, shape_areas, num_shapes):
            result += 1

    print(result)


if __name__ == '__main__':
    main()
