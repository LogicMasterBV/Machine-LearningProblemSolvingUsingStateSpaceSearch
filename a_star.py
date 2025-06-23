# A* search algorithm (Node, heuristic, step-by-step search)

import heapq
from constants import moves
from maze import is_valid
from constants import ROWS, COLS  # to ensure bounds

def get_neighbors(position):
    row, col = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            neighbors.append((r, c))

    return neighbors

class Node:
    def __init__(self, position, g, h, parent=None):
        self.position = position
        self.g = g # cost from the start node to this node
        self.h = h # heuristic estimate from this node to the goal
        self.f = g + h # total estimated cost of the cheapest path through this node
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f #f  is used to compare nodes in the priority queue (open_set)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return path[::-1]

def expand_node(current_node, open_set, visited, parents, open_dict, obstacles, goal):
    new_frontier = []
    neighbors = get_neighbors(current_node.position)
    for neighbor in neighbors:
        if neighbor in obstacles or neighbor in visited:
            continue
        tentative_g = current_node.g + 1
        if neighbor not in open_dict or tentative_g < open_dict[neighbor]:
            neighbor_node = Node(neighbor, tentative_g, heuristic(neighbor, goal), current_node)
            heapq.heappush(open_set, neighbor_node)
            open_dict[neighbor] = tentative_g
            parents[neighbor] = current_node.position
            new_frontier.append(neighbor)
    visited.add(current_node.position)
    return new_frontier

def print_path(label, path):
    print(f"{label}: [{' -> '.join(str(p) for p in path)}]")

def print_frontier(open_dict):
    print("Frontier:", list(open_dict.keys()))
