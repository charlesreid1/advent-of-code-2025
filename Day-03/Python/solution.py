def get_max_joltage_12_digits(s):
    k = 12
    n = len(s)
    if n < k:
        return 0
    
    result_digits = []
    current_search_start_idx = 0
    
    for i in range(k):
        # Calculate the actual end index for the current search window
        # The window must be large enough to guarantee k-i more characters to pick
        search_window_end_idx = n - (k - i) 
        
        search_slice = s[current_search_start_idx : search_window_end_idx + 1]
        max_digit_char = max(search_slice)
        max_digit_idx = s.index(max_digit_char, current_search_start_idx)
                
        result_digits.append(max_digit_char)
        current_search_start_idx = max_digit_idx + 1
        
    return int("".join(result_digits))


def part1(filename):
    total_output_joltage = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            max_bank_joltage = max((int(line[i] + line[j]) for i in range(len(line)) for j in range(i + 1, len(line))), default=0)

            total_output_joltage += max_bank_joltage

    print(total_output_joltage)


def part2(filename):
    with open(filename, 'r') as file:
        total_output_joltage = sum(
            get_max_joltage_12_digits(line.strip())
            for line in file
            if line.strip() and len(line.strip()) >= 12
        )

    print(total_output_joltage)

if __name__=="__main__":
    part1("example")
    part1("input")
    part2("example")
    part2("input")
