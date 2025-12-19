from pathlib import Path
import re
import math
import collections
from fractions import Fraction
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def parse_line_part2(line):
    # Extract button schematics
    schematics_matches = re.findall(r'\((.*?)\)', line)
    button_schematics = []
    for s_str in schematics_matches:
        if s_str: 
            schematic = list(map(int, s_str.split(',')))
            button_schematics.append(schematic)
        else:
            button_schematics.append([]) 

    # Extract joltage requirements
    joltage_match = re.search(r'\{(.*?)\}', line)
    if not joltage_match:
        raise ValueError(f"Joltage requirements not found in line: {line}")
    joltage_str = joltage_match.group(1)
    target_joltage = list(map(int, joltage_str.split(',')))
    num_counters = len(target_joltage)

    return target_joltage, button_schematics, num_counters

def solve_machine_milp(target_joltage, button_schematics, num_counters):
    num_buttons = len(button_schematics)
    
    # 1. Build the Coefficient Matrix A
    # A[i][j] = 1 if button j affects counter i, else 0
    A = np.zeros((num_counters, num_buttons))
    for j, schematic in enumerate(button_schematics):
        for counter_idx in schematic:
            A[counter_idx, j] = 1
            
    # 2. Define the Objective: Minimize sum of x_i
    # c = [1, 1, ..., 1]
    c = np.ones(num_buttons)
    
    # 3. Define Constraints: A @ x = target_joltage
    # We use LinearConstraint with equal lower and upper bounds to enforce equality
    b = np.array(target_joltage)
    constraints = LinearConstraint(A, b, b)
    
    # 4. Define Integrality: 1 means integer constraint
    integrality = np.ones(num_buttons)
    
    # 5. Define Bounds: 0 <= x <= infinity
    bounds = Bounds(lb=0, ub=np.inf)
    
    # 6. Solve
    res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    
    if res.success:
        # result.x gives the optimal button presses
        # We round to nearest integer to avoid floating point drift (e.g. 3.00000001)
        return int(np.round(np.sum(res.x)))
    else:
        # If the status is 2 (infeasible), no solution exists
        return float('inf')

def part2(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    total_min_presses = 0
    with open(f, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            target_joltage, button_schematics, num_counters = parse_line_part2(line)
            
            min_presses = solve_machine_milp(target_joltage, button_schematics, num_counters)
            
            if min_presses == float('inf'):
                # Some machines might be unsolvable, which is valid
                pass
            else:
                total_min_presses += min_presses

    print(total_min_presses)


###############################################
# The code below was from the first iteration.

# The `solve_machine_part2` function uses a Breadth-First Search (BFS) algorithm.
# While this approach is correct for finding the minimum presses, its performance
# degrades significantly as the target joltage values increase.
# For the 'example' input, where max joltage is 12, the BFS is efficient.
# However, for the 'input' file, maximum joltage values are up to ~245.
# With multiple counters (up to 10), the state space (max_joltage^num_counters)
# becomes too large (e.g., 245^10 is astronomically large) for the BFS to complete
# in a reasonable time, leading to the script getting stuck.
#
# A robust solution for such large target values with small N, M (buttons/counters)
# typically requires techniques from Integer Linear Programming (ILP) or solving
# systems of linear Diophantine equations (e.g., using integer Gaussian elimination
# to find a general solution and then optimizing parameters). Implementing such
# advanced mathematical solvers from scratch with standard Python libraries
# is beyond the practical scope and token limits of this environment.


def solve_machine_part2(target_joltage, button_schematics, num_counters):
    num_buttons = len(button_schematics)
    
    # Initial state: all counters at 0
    initial_joltage_state = tuple([0] * num_counters)
    
    # Queue for BFS: (current_joltage_state_tuple, total_presses)
    queue = collections.deque([(initial_joltage_state, 0)])
    
    # Dictionary to store the minimum presses to reach a given joltage state
    # This acts as both visited set and distance map
    min_presses_to_state = {initial_joltage_state: 0}
    
    while queue:
        current_jv_tuple, current_presses = queue.popleft()

        # If we reached the target, return immediately as BFS guarantees shortest path
        if list(current_jv_tuple) == target_joltage:
            return current_presses
        
        # Explore pressing each button once
        for button_idx in range(num_buttons):
            button_effects = button_schematics[button_idx]
            next_jv_list = list(current_jv_tuple)
            is_valid_transition = True

            # Apply the effect of pressing this button once
            for counter_idx in button_effects:
                next_jv_list[counter_idx] += 1
                # Check if this press exceeds the target for any counter
                if next_jv_list[counter_idx] > target_joltage[counter_idx]:
                    is_valid_transition = False
                    break
            
            if is_valid_transition:
                next_jv_tuple = tuple(next_jv_list)
                next_presses = current_presses + 1

                # If this state hasn't been visited, or we found a shorter path to it
                if next_jv_tuple not in min_presses_to_state or next_presses < min_presses_to_state[next_jv_tuple]:
                    min_presses_to_state[next_jv_tuple] = next_presses
                    queue.append((next_jv_tuple, next_presses))
                    
    return float('inf') # Target not reachable


def part2_bruteforcedfs(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    total_min_presses = 0
    with open(f, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            target_joltage, button_schematics, num_counters = parse_line_part2(line)
            
            min_for_this_machine = solve_machine_part2(target_joltage, button_schematics, num_counters)
            
            if min_for_this_machine == float('inf'):
                print(f"Warning: Could not configure machine for Part 2: {line}")
            else:
                total_min_presses += min_for_this_machine

    print(total_min_presses)

