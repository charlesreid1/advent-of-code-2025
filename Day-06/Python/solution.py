from pathlib import Path
import math

def solve_problem(numbers, operator):
    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        return math.prod(numbers)
    else:
        raise ValueError(f"Unknown operator: {operator}")

def part1(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    with open(f, 'r') as file:
        # Read lines, stripping trailing whitespace to handle input like "123 "
        # but keep leading whitespace for alignment purposes during parsing
        lines = [line.rstrip() for line in file] 

    # Determine maximum line length for consistent padding
    max_len = max(len(line) for line in lines)

    # Pad all lines to the maximum length to ensure uniform grid for column processing
    padded_lines = [line.ljust(max_len) for line in lines]

    # Identify indices of columns that are entirely composed of spaces across all lines.
    # These act as visual separators between problems.
    separator_indices = []
    for j in range(max_len):
        is_separator_col = True
        for i in range(len(padded_lines)):
            if padded_lines[i][j] != ' ':
                is_separator_col = False
                break
        if is_separator_col:
            separator_indices.append(j)

    # Use identified separator indices to define the horizontal start and end columns for each problem block.
    problem_ranges = []
    start_col = 0
    for sep_idx in separator_indices:
        if sep_idx > start_col:
            problem_ranges.append((start_col, sep_idx))
        start_col = sep_idx + 1
    
    # Capture the last problem block if it extends to the end of the input grid.
    if start_col < max_len:
        problem_ranges.append((start_col, max_len))
    
    grand_total = 0

    # Process each identified problem block
    for start, end in problem_ranges:
        # Extract the relevant character slice for the current problem block from each line
        problem_block_lines = [line[start:end] for line in padded_lines]
        
        # The last line of each problem block contains the operator symbol.
        operator_char = problem_block_lines[-1].strip()
        
        # The lines above the operator contain the numbers for the problem.
        numbers_str_lines = problem_block_lines[:-1]
        
        numbers = []
        for s in numbers_str_lines:
            stripped_s = s.strip()
            if stripped_s: # Convert to int only if the stripped string is not empty
                numbers.append(int(stripped_s))
        
        if not numbers: # Skip problem blocks that somehow ended up without numbers (e.g., just a separator or malformed input)
            continue

        problem_result = solve_problem(numbers, operator_char)
        grand_total += problem_result
    
    print(grand_total)

def part2(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    with open(f, 'r') as file:
        # Read lines, stripping trailing whitespace to handle input like "123 "
        # but keep leading whitespace for alignment purposes during parsing
        lines = [line.rstrip() for line in file] 

    # Determine maximum line length for consistent padding
    max_len = max(len(line) for line in lines)

    # Pad all lines to the maximum length to ensure uniform grid for column processing
    padded_lines = [line.ljust(max_len) for line in lines]

    # Identify indices of columns that are entirely composed of spaces across all lines.
    # These act as visual separators between problems.
    separator_indices = []
    for j in range(max_len):
        is_separator_col = True
        for i in range(len(padded_lines)):
            if padded_lines[i][j] != ' ':
                is_separator_col = False
                break
        if is_separator_col:
            separator_indices.append(j)

    # Use identified separator indices to define the horizontal start and end columns for each problem block.
    problem_ranges = []
    start_col = 0
    for sep_idx in separator_indices:
        if sep_idx > start_col:
            problem_ranges.append((start_col, sep_idx))
        start_col = sep_idx + 1
    
    # Capture the last problem block if it extends to the end of the input grid.
    if start_col < max_len:
        problem_ranges.append((start_col, max_len))
    
    grand_total = 0

    # Process each identified problem block in reverse order
    for start, end in reversed(problem_ranges):
        # Extract the relevant character slice for the current problem block from each line
        problem_block_lines = [line[start:end] for line in padded_lines]
        
        # The last line of each problem block contains the operator symbol.
        operator_char = problem_block_lines[-1].strip()
        
        # The lines above the operator contain the numbers for the problem.
        numbers_str_lines = problem_block_lines[:-1]
        
        # Filter out empty lines, then find the max length for internal padding
        filtered_numbers_str_lines = [s.strip() for s in numbers_str_lines if s.strip()]
        if not filtered_numbers_str_lines:
            continue

        # Determine the maximum length of numbers within this specific problem block
        # This handles cases where numbers might have different lengths within the same block
        max_internal_len = 0
        for line in numbers_str_lines:
            # We need to consider the actual content length, not just the stripped length
            # to preserve alignment for vertical reading.
            # Find the last non-space character in the segment to determine its effective length
            trimmed_line = line.rstrip()
            if trimmed_line:
                max_internal_len = max(max_internal_len, len(trimmed_line))
        
        # If no numbers found or max_internal_len is 0, skip
        if max_internal_len == 0:
            continue

        # Pad numbers_str_lines to max_internal_len on the left for correct transposition.
        # This ensures that digits align correctly when read vertically.
        padded_internal_numbers = [line.rjust(max_internal_len) for line in numbers_str_lines]
        
        # Transpose the numbers_str_lines to read numbers vertically
        transposed_numbers = []
        for i in range(max_internal_len): # Iterate over columns
            current_number_str = ""
            for j in range(len(padded_internal_numbers)): # Iterate over rows
                char = padded_internal_numbers[j][i]
                if char.isdigit():
                    current_number_str += char
            if current_number_str:
                transposed_numbers.append(int(current_number_str))
        
        if not transposed_numbers: # Skip if no numbers were formed after transposition
            continue

        problem_result = solve_problem(transposed_numbers, operator_char)
        grand_total += problem_result
    
    print(grand_total)


if __name__ == "__main__":
    part1('example')
    part1('input')
    part2('example')
    part2('input')


