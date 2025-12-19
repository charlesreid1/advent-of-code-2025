from pathlib import Path
import re
import math
import collections
from fractions import Fraction


def parse_line_part1(line):
    # Example line: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    # Extract diagram
    diagram_match = re.match(r'\[(.*?)\]', line)
    diagram_str = diagram_match.group(1)
    target_state = [1 if c == '#' else 0 for c in diagram_str]
    num_lights = len(target_state)

    # Extract button schematics
    schematics_matches = re.findall(r'\((.*?)\)', line)
    button_schematics = []
    for s_str in schematics_matches:
        if s_str: # Check if string is not empty (e.g., for empty tuple "()")
            schematic = list(map(int, s_str.split(',')))
            button_schematics.append(schematic)
        else:
            button_schematics.append([]) # Handle empty schematic (button toggles nothing)
    
    # Joltage requirements are ignored

    return target_state, button_schematics, num_lights

def solve_machine_part1(target_state, button_schematics, num_lights):
    num_buttons = len(button_schematics)
    min_presses_for_machine = float('inf')

    # Iterate through all 2^num_buttons combinations of button presses
    for i in range(1 << num_buttons): # i goes from 0 to 2^num_buttons - 1
        current_lights = [0] * num_lights # Lights initially off
        press_count = 0
        
        # Determine which buttons are pressed (odd number of times)
        button_press_combination = []
        for button_idx in range(num_buttons):
            if (i >> button_idx) & 1: # If the bit is set, this button is "pressed"
                button_press_combination.append(1)
                press_count += 1
            else:
                button_press_combination.append(0)

        # Apply the button presses to the current lights
        for button_idx in range(num_buttons):
            if button_press_combination[button_idx] == 1:
                for light_idx in button_schematics[button_idx]:
                    if 0 <= light_idx < num_lights: # Ensure light_idx is within bounds
                        current_lights[light_idx] = 1 - current_lights[light_idx] # Toggle

        # Check if the target state is reached
        if current_lights == target_state:
            min_presses_for_machine = min(min_presses_for_machine, press_count)
    
    return min_presses_for_machine

def part1(filename):
    f = Path(__file__).resolve().parent.parent / filename
    
    total_min_presses = 0
    try:
        with open(f, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                target_state, button_schematics, num_lights = parse_line_part1(line)
                
                min_for_this_machine = solve_machine_part1(target_state, button_schematics, num_lights)
                
                if min_for_this_machine == float('inf'):
                    print(f"Warning: Could not configure machine: {line}")
                else:
                    total_min_presses += min_for_this_machine

    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
        return
    except Exception as e:
        print(f"Error processing file '{filename}': {e}")
        return

    print(total_min_presses)


