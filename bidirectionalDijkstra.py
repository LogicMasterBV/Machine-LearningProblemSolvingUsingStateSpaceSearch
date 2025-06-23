# Bidirectional Dijkstra Maze Solver with Full GUI and Console Output

import heapq
import sys
import copy
import pygame
import math
import random

# Configuration
ROWS, COLS = 5, 6
CELL_SIZE = 80
BUTTON_HEIGHT = 50
BUTTON_GAP = 20
NUM_BUTTON_ROWS = 2
WINDOW_HEIGHT = ROWS * CELL_SIZE + NUM_BUTTON_ROWS * BUTTON_HEIGHT + BUTTON_GAP + 50

start = (0, 0)
goal = (4, 5)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DEFAULT_OBSTACLES = {(0, 1), (2, 1), (3, 1), (2, 3), (3, 4), (4, 4)}

# Validate cell

def is_valid(pos, obstacles):
    r, c = pos
    return 0 <= r < ROWS and 0 <= c < COLS and pos not in obstacles

# BFS solvability check
def is_solvable(start, goal, obstacles, rows, cols):
    from collections import deque
    queue = deque([start])
    visited = {start}
    while queue:
        current = queue.popleft()
        if current == goal:
            return True
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and neighbor not in obstacles and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return False

# Random solvable maze
def generate_random_obstacles(start, goal, rows, cols, num_obstacles):
    all_cells = [(r, c) for r in range(rows) for c in range(cols)]
    all_cells.remove(start)
    all_cells.remove(goal)
    while True:
        obstacles = set(random.sample(all_cells, num_obstacles))
        if is_solvable(start, goal, obstacles, rows, cols):
            return obstacles

# Draw arrow between cells
def draw_arrow(screen, from_cell, to_cell, color=(100, 100, 255)):
    fx, fy = from_cell[1] * CELL_SIZE + CELL_SIZE // 2, from_cell[0] * CELL_SIZE + CELL_SIZE // 2
    tx, ty = to_cell[1] * CELL_SIZE + CELL_SIZE // 2, to_cell[0] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(screen, color, (fx, fy), (tx, ty), 4)
    angle = math.atan2(ty - fy, tx - fx)
    arrow_size = 14
    for delta in [-0.4, 0.4]:
        end_x = tx - arrow_size * math.cos(angle + delta)
        end_y = ty - arrow_size * math.sin(angle + delta)
        pygame.draw.line(screen, color, (tx, ty), (end_x, end_y), 4)

# Grid drawing with states
def draw_grid(screen, visited_fwd, visited_bwd, path, parents_fwd, parents_bwd, obstacles, meet_node):
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pos = (r, c)
            if pos in obstacles:
                color = (0, 0, 0)
            elif pos == start:
                color = (0, 255, 0)
            elif pos == goal:
                color = (255, 0, 0)
            elif pos in path:
                color = (0, 0, 255)
            elif pos == meet_node:
                color = (255, 215, 0)
            elif pos in visited_fwd:
                color = (180, 220, 255)
            elif pos in visited_bwd:
                color = (255, 200, 220)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    for pos in visited_fwd:
        parent = parents_fwd.get(pos)
        if parent:
            draw_arrow(screen, parent, pos, color=(100, 120, 255))
    for pos in visited_bwd:
        parent = parents_bwd.get(pos)
        if parent:
            draw_arrow(screen, parent, pos, color=(255, 100, 120))

# Button rendering
def draw_buttons(screen):
    font = pygame.font.SysFont(None, 32)
    width = COLS * CELL_SIZE
    top_y = ROWS * CELL_SIZE
    step_rect = pygame.Rect(width//2 - 170 - 10, top_y, 150, BUTTON_HEIGHT)
    back_rect = pygame.Rect(width//2 + 10, top_y, 150, BUTTON_HEIGHT)
    rand_rect = pygame.Rect(width//2 - 170 - 10, top_y + BUTTON_HEIGHT + BUTTON_GAP, 150, BUTTON_HEIGHT)
    def_rect = pygame.Rect(width//2 + 10, top_y + BUTTON_HEIGHT + BUTTON_GAP, 150, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (70, 180, 70), step_rect)
    pygame.draw.rect(screen, (60, 100, 200), back_rect)
    pygame.draw.rect(screen, (180, 100, 20), rand_rect)
    pygame.draw.rect(screen, (100, 60, 180), def_rect)
    for rect, text in [(step_rect, "Step"), (back_rect, "Back"),
                       (rand_rect, "Randomize"), (def_rect, "Default Maze")]:
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
    pygame.display.flip()
    return step_rect, back_rect, rand_rect, def_rect

# Path reconstruction
def reconstruct_path(meet, parents_fwd, parents_bwd):
    path_fwd, path_bwd = [], []
    curr = meet
    while curr:
        path_fwd.append(curr)
        curr = parents_fwd.get(curr)
    path_fwd.reverse()
    curr = parents_bwd.get(meet)
    while curr:
        path_bwd.append(curr)
        curr = parents_bwd.get(curr)
    return path_fwd + path_bwd

# Main visualizer
def bidirectional_dijkstra_gui(start, goal):
    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_SIZE, WINDOW_HEIGHT))
    pygame.display.set_caption("Bidirectional Dijkstra Visualizer")
    clock = pygame.time.Clock()

    def reset_all(obstacles):
        open_fwd, open_bwd = [], []
        heapq.heappush(open_fwd, (0, start))
        heapq.heappush(open_bwd, (0, goal))
        visited_fwd, visited_bwd = {start: 0}, {goal: 0}
        parents_fwd, parents_bwd = {start: None}, {goal: None}
        meet_node, final_path, found = None, [], False
        history = [(copy.deepcopy(open_fwd), copy.deepcopy(open_bwd),
                    copy.deepcopy(visited_fwd), copy.deepcopy(visited_bwd),
                    copy.deepcopy(parents_fwd), copy.deepcopy(parents_bwd),
                    meet_node, found, copy.deepcopy(final_path))]
        return open_fwd, open_bwd, visited_fwd, visited_bwd, parents_fwd, parents_bwd, meet_node, found, final_path, history

    obstacles = generate_random_obstacles(start, goal, ROWS, COLS, 8)
    open_fwd, open_bwd, visited_fwd, visited_bwd, parents_fwd, parents_bwd, meet_node, found, final_path, history = reset_all(obstacles)
    expand_forward = True

    while True:
        screen.fill((220, 220, 220))
        draw_grid(screen, visited_fwd, visited_bwd, final_path, parents_fwd, parents_bwd, obstacles, meet_node)
        step_rect, back_rect, rand_rect, def_rect = draw_buttons(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if step_rect.collidepoint(event.pos) and not found:
                    history.append((copy.deepcopy(open_fwd), copy.deepcopy(open_bwd),
                                    copy.deepcopy(visited_fwd), copy.deepcopy(visited_bwd),
                                    copy.deepcopy(parents_fwd), copy.deepcopy(parents_bwd),
                                    meet_node, found, copy.deepcopy(final_path)))
                    if expand_forward and open_fwd:
                        g_fwd, node_fwd = heapq.heappop(open_fwd)
                        print(f"[Forward] Expanding: {node_fwd}, Cost: {g_fwd}")
                        for move in moves:
                            neighbor = (node_fwd[0] + move[0], node_fwd[1] + move[1])
                            if is_valid(neighbor, obstacles) and (neighbor not in visited_fwd or g_fwd + 1 < visited_fwd[neighbor]):
                                visited_fwd[neighbor] = g_fwd + 1
                                parents_fwd[neighbor] = node_fwd
                                heapq.heappush(open_fwd, (g_fwd + 1, neighbor))
                                print(f" -> Forward adding: {neighbor}, Cost: {g_fwd + 1}")
                                if neighbor in visited_bwd:
                                    total = visited_fwd[neighbor] + visited_bwd[neighbor]
                                    if meet_node is None or total < visited_fwd[meet_node] + visited_bwd[meet_node]:
                                        meet_node, found = neighbor, True
                    elif not expand_forward and open_bwd:
                        g_bwd, node_bwd = heapq.heappop(open_bwd)
                        print(f"[Backward] Expanding: {node_bwd}, Cost: {g_bwd}")
                        for move in moves:
                            neighbor = (node_bwd[0] + move[0], node_bwd[1] + move[1])
                            if is_valid(neighbor, obstacles) and (neighbor not in visited_bwd or g_bwd + 1 < visited_bwd[neighbor]):
                                visited_bwd[neighbor] = g_bwd + 1
                                parents_bwd[neighbor] = node_bwd
                                heapq.heappush(open_bwd, (g_bwd + 1, neighbor))
                                print(f" -> Backward adding: {neighbor}, Cost: {g_bwd + 1}")
                                if neighbor in visited_fwd:
                                    total = visited_fwd[neighbor] + visited_bwd[neighbor]
                                    if meet_node is None or total < visited_fwd[meet_node] + visited_bwd[meet_node]:
                                        meet_node, found = neighbor, True
                    if meet_node and found:
                        final_path = reconstruct_path(meet_node, parents_fwd, parents_bwd)
                        print(f"Meeting node: {meet_node}")
                        print("Final Path:", final_path)
                        print(f"Path length: {len(final_path) - 1}")
                    expand_forward = not expand_forward

                elif back_rect.collidepoint(event.pos) and len(history) > 1:
                    history.pop()
                    open_fwd, open_bwd, visited_fwd, visited_bwd, parents_fwd, parents_bwd, meet_node, found, final_path = copy.deepcopy(history[-1])
                    expand_forward = not expand_forward

                elif rand_rect.collidepoint(event.pos):
                    obstacles = generate_random_obstacles(start, goal, ROWS, COLS, 8)
                    open_fwd, open_bwd, visited_fwd, visited_bwd, parents_fwd, parents_bwd, meet_node, found, final_path, history = reset_all(obstacles)
                    expand_forward = True

                elif def_rect.collidepoint(event.pos):
                    obstacles = set(DEFAULT_OBSTACLES)
                    open_fwd, open_bwd, visited_fwd, visited_bwd, parents_fwd, parents_bwd, meet_node, found, final_path, history = reset_all(obstacles)
                    expand_forward = True

        clock.tick(60)

if __name__ == '__main__':
    bidirectional_dijkstra_gui(start, goal)