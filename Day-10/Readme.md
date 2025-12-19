# Advent of Code Day 10 Part b

## Problem Analysis

In Part 2, we are given machines with specific joltage requirements (counters) and buttons that increment specific
counters. We start at zero and must reach exact target values (e.g., 25, 47, ...) by pressing buttons.

Goal: Minimize the number of button presses.

Because the target numbers in the real input are large (~250) and there are up to 10 buttons/counters, the state
space is too large for standard search algorithms like BFS or DFS (250^10 states)

## Mathematical formulation

Let x_j be the number of times we press button j. 

Let t_ibe the target joltage for counter i. 

Let Aij = 1 if button j increments counter i, and 0 otherwise.

We want to:

1. Minimize sum(x_j) (total button presses)
2. Subject to Ax = t (buttons must exactly match targets)
3. Constraints x_j >= 0 and x_j in integers Z (cnanot press negative/fractional times)

Solution approach:

Utilize scipy.optimize.milp to solve this efficiently using branch-and-cut algorithms.

## Why this works

* milp reduces the state space (instead of simulating button presses, which is very slow for large inputs)
* if there are multiple ways to reach the target (underdetermined systems), solver automatically selects
  combination minimizing objective function (∑x).
* if machine cannot physically reach target (i.e., odd number using only buttons that add to 2), solver detects
  this condition immediately, returns failure status, making it run fast

