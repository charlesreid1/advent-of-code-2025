# Day 4: Printing Department — JavaScript

## Requirements

- [Node.js](https://nodejs.org/)

## Usage

Pipe your input file into the script:

```bash
node solution.js < input.txt
```

Or use your shell's input redirection however you prefer. The script reads from stdin and prints two lines:

- **Line 1** — Part 1 answer (count of paper rolls `@` accessible from the start — fewer than 4 adjacent `@` symbols).
- **Line 2** — Part 2 answer (total rolls removed across all iterations, where each iteration removes every roll with fewer than 4 adjacent `@` until none remain).
