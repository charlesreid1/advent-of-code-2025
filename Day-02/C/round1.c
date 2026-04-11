#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <ctype.h>

typedef struct {
    uint64_t start;
    uint64_t end;
} Range;

// Parse ranges from input string
Range* parse_ranges(const char* input, int* num_ranges) {
    // Count commas to estimate number of ranges
    int count = 1;
    for (const char* p = input; *p; p++) {
        if (*p == ',') count++;
    }

    Range* ranges = malloc(count * sizeof(Range));
    if (!ranges) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    char* copy = strdup(input);
    char* token = strtok(copy, ",");
    int i = 0;

    while (token) {
        char* dash = strchr(token, '-');
        if (!dash) {
            fprintf(stderr, "Invalid range format: %s\n", token);
            free(copy);
            free(ranges);
            exit(1);
        }

        *dash = '\0';
        ranges[i].start = strtoull(token, NULL, 10);
        ranges[i].end = strtoull(dash + 1, NULL, 10);
        i++;
        token = strtok(NULL, ",");
    }

    *num_ranges = i;
    free(copy);
    return ranges;
}

// Check if a number is within any range
bool is_in_range(uint64_t num, Range* ranges, int num_ranges) {
    for (int i = 0; i < num_ranges; i++) {
        if (num >= ranges[i].start && num <= ranges[i].end) {
            return true;
        }
    }
    return false;
}

// Generate invalid IDs (numbers made of digits repeated twice)
uint64_t generate_invalid_ids(Range* ranges, int num_ranges) {
    uint64_t total = 0;

    // For k-digit numbers (k from 1 to 6, since 6-digit repeated twice = 12 digits max)
    for (int k = 1; k <= 6; k++) {
        uint64_t start = (k == 1) ? 1 : 1;
        for (int i = 0; i < k - 1; i++) start *= 10;

        uint64_t end = 1;
        for (int i = 0; i < k; i++) end *= 10;

        for (uint64_t x = start; x < end; x++) {
            // Create number by repeating x twice
            char buf1[32], buf2[64];
            snprintf(buf1, sizeof(buf1), "%llu", x);
            snprintf(buf2, sizeof(buf2), "%s%s", buf1, buf1);

            uint64_t invalid_id = strtoull(buf2, NULL, 10);

            if (is_in_range(invalid_id, ranges, num_ranges)) {
                total += invalid_id;
            }
        }
    }

    return total;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE* file = fopen(argv[1], "r");
    if (!file) {
        fprintf(stderr, "Could not open file: %s\n", argv[1]);
        return 1;
    }

    // Read entire file
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* input = malloc(file_size + 1);
    if (!input) {
        fprintf(stderr, "Memory allocation failed\n");
        fclose(file);
        return 1;
    }

    fread(input, 1, file_size, file);
    input[file_size] = '\0';
    fclose(file);

    // Remove whitespace
    char* p = input;
    char* q = input;
    while (*p) {
        if (!isspace((unsigned char)*p)) {
            *q++ = *p;
        }
        p++;
    }
    *q = '\0';

    int num_ranges;
    Range* ranges = parse_ranges(input, &num_ranges);

    uint64_t result = generate_invalid_ids(ranges, num_ranges);
    printf("%llu\n", result);

    free(input);
    free(ranges);
    return 0;
}