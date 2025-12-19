from pathlib import Path
import bisect


def part1(filename):
    """
    Parses an inventory database, determines which ingredients are fresh,
    and prints the total count of fresh ingredients.

    The database consists of fresh ingredient ID ranges and a list of
    available ingredient IDs, separated by a blank line.

    Args:
        filename (str): The path to the input database file.
    """
    
    # 1. Parse Input
    ranges_str = []
    ids_str = []
    is_range_section = True
    
    f = Path(__file__).resolve().parent.parent / filename
    try:
        with open(f, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    is_range_section = False
                    continue
                
                if is_range_section:
                    ranges_str.append(line)
                else:
                    ids_str.append(line)
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return

    ranges = []
    for r_str in ranges_str:
        try:
            start, end = map(int, r_str.split('-'))
            ranges.append((start, end))
        except ValueError:
            continue
            
    ids = []
    for id_str in ids_str:
        try:
            ids.append(int(id_str))
        except ValueError:
            continue

    # 2. Merge Ranges
    merged = []
    if ranges:
        ranges.sort()
        merged = [ranges[0]]
        for i in range(1, len(ranges)):
            current_start, current_end = ranges[i]
            last_start, last_end = merged[-1]
            if current_start <= last_end:
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                merged.append((current_start, current_end))

    # 3. Count Fresh Ingredients
    fresh_count = 0
    if merged:
        start_points = [r[0] for r in merged]
        for an_id in ids:
            pos = bisect.bisect_right(start_points, an_id)
            if pos > 0:
                check_range = merged[pos - 1]
                if check_range[0] <= an_id <= check_range[1]:
                    fresh_count += 1
                    
    # 4. Print Solution
    print(fresh_count)


def part2(filename):
    """
    Parses fresh ingredient ID ranges, merges them, and counts the
    total number of unique fresh ingredient IDs.

    Args:
        filename (str): The path to the input database file.
    """
    ranges_str = []

    f = Path(__file__).resolve().parent.parent / filename
    try:
        with open(f, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    # Stop reading at the blank line separator
                    break
                ranges_str.append(line)
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return

    ranges = []
    for r_str in ranges_str:
        try:
            start, end = map(int, r_str.split('-'))
            ranges.append((start, end))
        except ValueError:
            continue

    if not ranges:
        print(0)
        return

    # Merge Overlapping Ranges (same logic as part1)
    ranges.sort()
    merged = [ranges[0]]
    for i in range(1, len(ranges)):
        current_start, current_end = ranges[i]
        last_start, last_end = merged[-1]
        if current_start <= last_end:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    # Calculate Total Fresh IDs from Merged Ranges
    total_fresh_count = 0
    for start, end in merged:
        total_fresh_count += (end - start + 1)

    print(total_fresh_count)


if __name__ == "__main__":
    part1('example')
    part1('input')
    part2('example')
    part2('input')

