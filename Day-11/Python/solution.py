from pathlib import Path
from collections import defaultdict

def parse_graph(filename):
    graph = defaultdict(list)
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(':')
                if len(parts) != 2:
                    continue # Malformed line
                
                source = parts[0].strip()
                destinations = parts[1].strip().split()
                
                for dest in destinations:
                    graph[source].append(dest)
    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return None
    except Exception as e:
        print(f"Error parsing file '{filename}': {e}")
        return None
    
    return graph

def count_paths(start_node, end_node, graph, memo):
    # If already computed, return memoized result
    if (start_node, end_node) in memo:
        return memo[(start_node, end_node)]
    
    # Base case: If start_node is the end_node, we found one path
    if start_node == end_node:
        return 1
    
    # If start_node has no outgoing edges and is not the end_node, no paths from here
    if start_node not in graph:
        return 0
        
    total_paths = 0
    # Recursively count paths from neighbors
    for neighbor in graph[start_node]:
        total_paths += count_paths(neighbor, end_node, graph, memo)
    
    # Memoize and return result
    memo[(start_node, end_node)] = total_paths
    return total_paths


def part1(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    graph = parse_graph(f)
    if graph is None:
        return

    memo = {}
    result = count_paths('you', 'out', graph, memo)
    print(result)

# New function for part2
def count_paths_with_targets(current_node, end_node, graph, target1, target2, visited_target1, visited_target2, memo):
    # Update visited flags if current_node is one of the targets
    if current_node == target1:
        visited_target1 = True
    if current_node == target2:
        visited_target2 = True

    # Memoization key
    memo_key = (current_node, visited_target1, visited_target2)
    if memo_key in memo:
        return memo[memo_key]

    # Base case: If we reached the end_node
    if current_node == end_node:
        # Only count this path if both targets have been visited
        return 1 if visited_target1 and visited_target2 else 0

    # If current_node has no outgoing edges, or is not in graph (a sink node), no paths from here
    if current_node not in graph:
        return 0

    total_paths = 0
    # Recursively count paths from neighbors
    for neighbor in graph[current_node]:
        total_paths += count_paths_with_targets(neighbor, end_node, graph, target1, target2, visited_target1, visited_target2, memo)

    # Memoize and return result
    memo[memo_key] = total_paths
    return total_paths

def part2(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    graph = parse_graph(f)
    if graph is None:
        return

    memo = {}
    # Initial call: from 'svr' to 'out', requiring 'dac' and 'fft', neither visited yet
    result = count_paths_with_targets('svr', 'out', graph, 'dac', 'fft', False, False, memo)
    print(result)

if __name__ == "__main__":
    part1('example_part1')
    part1('input')
    part2('example_part2')
    part2('input')
