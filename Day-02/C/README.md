# Day 2: Gift Shop - C Implementation

This is a C implementation of the Advent of Code 2025 Day 2 problem "Gift Shop".

## Problem Description

The program identifies invalid product IDs in given ranges. An invalid ID is any number made only of some sequence of digits repeated twice (e.g., 55, 6464, 123123). The program reads ranges from an input file and sums all invalid IDs that fall within those ranges.

## Files

- `round1.c` - Clean C implementation
- `round2.c` - Obfuscated version
- `Makefile` - Build automation
- `README.md` - This file

## Building

### Clean version (round1):
```bash
gcc -o round1 round1.c -Wall -Wextra -O2
```

### Obfuscated version (round2):
```bash
gcc -o round2 round2.c -Wall -Wextra -O2
```

### Using Makefile:
```bash
make              # Builds round1
make clean        # Clean all executables
make test         # Test round1 with example input
```

## Usage

```bash
./round1 <input_file>
```

The input file should contain ranges in the format:
```
start1-end1,start2-end2,start3-end3,...
```

Example:
```
11-22,95-115,998-1012,1188511880-1188511890
```

## Example

Given the example input from the problem statement:

```
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
```

The program outputs:
```
1227775554
```

Which matches the expected result from the problem.

## Algorithm

1. **Parse ranges**: Read and parse the comma-separated ranges from the input file
2. **Generate invalid IDs**: For k-digit numbers (k from 1 to 6):
   - Generate all k-digit numbers x (without leading zeros)
   - Create invalid ID by concatenating x with itself: str(x) + str(x)
   - Convert back to integer
3. **Check ranges**: For each generated invalid ID, check if it falls within any input range
4. **Sum valid invalid IDs**: Sum all invalid IDs that are within ranges

## Performance Considerations

- The algorithm generates numbers up to 6 digits repeated twice (12-digit numbers max)
- Uses 64-bit integers (uint64_t) to handle large numbers
- Memory usage is O(n) where n is the number of ranges

## Testing

To test with the provided example:

```bash
./round1 ../example
```

Expected output: `1227775554`

## Obfuscated Version (Round 2)

The `round2.c` file contains an obfuscated version of the solution in the style of the International Obfuscated C Code Contest (IOCCC):

### Obfuscation techniques used:
1. **Structural obfuscation**: All functions merged into `main()`, complex conditional expressions
2. **Identifier obfuscation**: Single-letter and confusing variable names
3. **Code compression**: Minimal whitespace, combined statements
4. **Visual shaping**: `round2.c` is formatted to visually resemble a Christmas tree when viewed in a monospace editor

### Verification:
Obfuscated version produces identical output to the clean implementation:
```bash
./round2 ../example          # Output: 1227775554
```
