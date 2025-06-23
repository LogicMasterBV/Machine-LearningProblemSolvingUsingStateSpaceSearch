# Maze generation, solvability checking

import random
from collections import deque
from constants import moves

def is_valid(pos, rows, cols, obstacles):
    r, c = pos
    return 0 <= r < rows and 0 <= c < cols and pos not in obstacles

def generate_random_obstacles(start, goal, rows, cols, num_obstacles):
    all_cells = [(r, c) for r in range(rows) for c in range(cols)]
    all_cells.remove(start)
    all_cells.remove(goal)
    while True:
        obstacles = set(random.sample(all_cells, num_obstacles))
        if is_solvable(start, goal, obstacles, rows, cols):
            return obstacles

def is_solvable(start, goal, obstacles, rows, cols):
    queue = deque([start])
    visited = {start}
    while queue:
        current = queue.popleft()
        if current == goal:
            return True
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if (
                0 <= neighbor[0] < rows and
                0 <= neighbor[1] < cols and
                neighbor not in obstacles and
                neighbor not in visited
            ):
                visited.add(neighbor)
                queue.append(neighbor)
    return False
