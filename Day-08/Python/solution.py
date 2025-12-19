from pathlib import Path
import math
from collections import defaultdict

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n # To store the size of each set/circuit

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Union by size heuristic
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True
        return False

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)

def part1(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    coordinates = []
    try:
        with open(f, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    x, y, z = map(int, line.split(','))
                    coordinates.append((x, y, z))
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return
    except ValueError:
        print(f"Error: Invalid coordinate format in '{filename}'")
        return

    num_junction_boxes = len(coordinates)
    if num_junction_boxes < 3:
        print("Not enough junction boxes to form circuits for multiplication.")
        return

    # 1. Calculate all pairwise distances
    distances = []
    for i in range(num_junction_boxes):
        for j in range(i + 1, num_junction_boxes):
            dist = calculate_distance(coordinates[i], coordinates[j])
            distances.append((dist, i, j))

    # 2. Sort pairs by distance
    distances.sort()

    # 3. Connect closest pairs using DSU
    dsu = DSU(num_junction_boxes)
    attempts_made = 0
    max_attempts = 1000 # Problem statement specifies 1000 connections
    
    if filename == 'example':
        max_attempts = 10 

    for dist, i, j in distances:
        if attempts_made >= max_attempts:
            break
        dsu.union(i, j) # Always attempt union, whether it changes the structure or not
        attempts_made += 1
            
    # 4. Determine circuit sizes
    circuit_sizes = defaultdict(int)
    for i in range(num_junction_boxes):
        root = dsu.find(i)
        circuit_sizes[root] = dsu.size[root]
    
    # 5. Multiply sizes of three largest circuits
    sorted_sizes = sorted(circuit_sizes.values(), reverse=True)

    if filename == 'example':
        print(f"Sorted circuit sizes for example: {sorted_sizes}")

    if len(sorted_sizes) < 3:
        print("Not enough circuits to multiply the three largest.")
        return

    result = sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]
    print(result)

def part2(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    coordinates = []
    try:
        with open(f, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    x, y, z = map(int, line.split(','))
                    coordinates.append((x, y, z))
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return
    except ValueError:
        print(f"Error: Invalid coordinate format in '{filename}'")
        return

    num_junction_boxes = len(coordinates)
    if num_junction_boxes < 2:
        print("Not enough junction boxes to form a circuit.")
        return

    # 1. Calculate all pairwise distances
    distances = []
    for i in range(num_junction_boxes):
        for j in range(i + 1, num_junction_boxes):
            dist = calculate_distance(coordinates[i], coordinates[j])
            distances.append((dist, i, j))

    # 2. Sort pairs by distance
    distances.sort()

    # 3. Connect closest pairs using DSU until all in one circuit
    dsu = DSU(num_junction_boxes)
    num_circuits = num_junction_boxes
    last_connected_coords = None

    for dist, i, j in distances:
        if num_circuits == 1: # All boxes are already in one circuit
            break
        
        # Check if i and j are already in the same set
        if dsu.find(i) != dsu.find(j):
            dsu.union(i, j)
            num_circuits -= 1
            # Only update last_connected_coords if a successful union occurred
            # and it results in the final single circuit.
            if num_circuits == 1:
                last_connected_coords = (coordinates[i], coordinates[j])
                break # Exit after forming the single circuit

    if last_connected_coords:
        x1 = last_connected_coords[0][0]
        x2 = last_connected_coords[1][0]
        result = x1 * x2
        print(result)
    else:
        print("Could not find the last connected pair to form a single circuit.")

if __name__ == "__main__":
    part1('example')
    part1('input')
    part2('example')
    part2('input')