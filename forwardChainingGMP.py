import pygame
import sys
import random
import copy
from collections import deque

# Config
ROWS, COLS = 5, 6
CELL_SIZE = 80
BUTTON_HEIGHT = 50
BUTTON_GAP = 20
NUM_BUTTON_ROWS = 2
WINDOW_HEIGHT = ROWS * CELL_SIZE + NUM_BUTTON_ROWS * BUTTON_HEIGHT + BUTTON_GAP + 50
WINDOW_WIDTH = COLS * CELL_SIZE

start = (0, 0)
goal = (4, 5)
DEFAULT_OBSTACLES = {(0, 1), (2, 1), (3, 1), (2, 3), (3, 4), (4, 4)}
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
NUM_OBSTACLES = 8

def is_valid(pos, obstacles):
    r, c = pos
    return 0 <= r < ROWS and 0 <= c < COLS and pos not in obstacles

def generate_can_move_rules(obstacles):
    rules = []
    for r in range(ROWS):
        for c in range(COLS):
            from_pos = (r, c)
            if from_pos in obstacles:
                continue
            for move in moves:
                to_pos = (r + move[0], c + move[1])
                if is_valid(to_pos, obstacles):
                    rules.append((from_pos, to_pos))
    return rules

def apply_gmp_step(facts, agenda, rules, parents, inference_chain):
    if not agenda:
        return False, None
    current = agenda.popleft()
    for (x, y) in rules:
        if x == current and y not in facts:
            facts.add(y)
            agenda.append(y)
            parents[y] = x
            inference_chain.append((x, y))
            rule_str = f"At{x} ∧ CanMove({x}, {y}) ⇒ At{y}"
            return True, (y, rule_str)
    return True, None

def reconstruct_path(parents, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parents.get(node)
    return path[::-1]

def generate_random_obstacles(start, goal, rows, cols, num_obstacles):
    all_cells = [(r, c) for r in range(rows) for c in range(cols)]
    all_cells.remove(start)
    all_cells.remove(goal)
    while True:
        obstacles = set(random.sample(all_cells, num_obstacles))
        if is_solvable(start, goal, obstacles):
            return obstacles

def is_solvable(start, goal, obstacles):
    queue = deque([start])
    visited = {start}
    while queue:
        current = queue.popleft()
        if current == goal:
            return True
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if is_valid(neighbor, obstacles) and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return False

def draw_grid(screen, facts, obstacles, inference_chain, current_rule, found, goal):
    font = pygame.font.SysFont(None, 26)
    for r in range(ROWS):
        for c in range(COLS):
            pos = (r, c)
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = (255, 255, 255)
            if pos in obstacles:
                color = (0, 0, 0)
            elif pos == start:
                color = (0, 255, 0)
            elif pos == goal:
                color = (255, 0, 0)
            elif pos in facts:
                color = (200, 200, 200)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    for src, dest in inference_chain:
        x1, y1 = src[1] * CELL_SIZE + CELL_SIZE // 2, src[0] * CELL_SIZE + CELL_SIZE // 2
        x2, y2 = dest[1] * CELL_SIZE + CELL_SIZE // 2, dest[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.line(screen, (128, 0, 128), (x1, y1), (x2, y2), 3)

    # Display inference rule text
    if current_rule:
        rule_txt = font.render(f"Rule applied: {current_rule}", True, (0, 0, 0))
        screen.blit(rule_txt, (10, ROWS * CELL_SIZE + 5))

def draw_buttons(screen):
    font = pygame.font.SysFont(None, 28)
    width = COLS * CELL_SIZE
    top_y = ROWS * CELL_SIZE + 35
    gap = BUTTON_GAP

    step_rect = pygame.Rect(width//2 - 170 - 10, top_y, 150, BUTTON_HEIGHT)
    back_rect = pygame.Rect(width//2 + 10, top_y, 150, BUTTON_HEIGHT)
    rand_rect = pygame.Rect(width//2 - 170 - 10, top_y + BUTTON_HEIGHT + gap, 150, BUTTON_HEIGHT)
    def_rect = pygame.Rect(width//2 + 10, top_y + BUTTON_HEIGHT + gap, 150, BUTTON_HEIGHT)

    pygame.draw.rect(screen, (70, 180, 70), step_rect)
    pygame.draw.rect(screen, (200, 100, 100), back_rect)
    pygame.draw.rect(screen, (100, 100, 200), rand_rect)
    pygame.draw.rect(screen, (100, 60, 180), def_rect)

    screen.blit(font.render("Step", True, (255,255,255)), (step_rect.centerx - 25, step_rect.centery - 10))
    screen.blit(font.render("Back", True, (255,255,255)), (back_rect.centerx - 25, back_rect.centery - 10))
    screen.blit(font.render("Randomize", True, (255,255,255)), (rand_rect.centerx - 50, rand_rect.centery - 10))
    screen.blit(font.render("Default Maze", True, (255,255,255)), (def_rect.centerx - 70, def_rect.centery - 10))

    return step_rect, back_rect, rand_rect, def_rect

def maze_solver_gmp_gui():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Solver using GMP (Forward Chaining)")
    clock = pygame.time.Clock()

    def reset(obstacles):
        facts = set([start])
        agenda = deque([start])
        parents = {start: None}
        inference_chain = []
        history = []
        found = False
        current_rule = None
        return facts, agenda, parents, inference_chain, history, found, current_rule

    current_obstacles = set(DEFAULT_OBSTACLES)
    facts, agenda, parents, inference_chain, history, found, current_rule = reset(current_obstacles)

    while True:
        screen.fill((230, 230, 230))
        draw_grid(screen, facts, current_obstacles, inference_chain, current_rule, found, goal)
        step_rect, back_rect, rand_rect, def_rect = draw_buttons(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if step_rect.collidepoint(event.pos):
                    if not found:
                        history.append((copy.deepcopy(facts), copy.deepcopy(agenda),
                                        copy.deepcopy(parents), copy.deepcopy(inference_chain), current_rule))
                        can_move_rules = generate_can_move_rules(current_obstacles)
                        progressed, result = apply_gmp_step(facts, agenda, can_move_rules, parents, inference_chain)
                        current_rule = result[1] if result else None
                        if result and result[0] == goal:
                            found = True

                elif back_rect.collidepoint(event.pos):
                    if history:
                        facts, agenda, parents, inference_chain, current_rule = history.pop()
                        found = goal in facts

                elif rand_rect.collidepoint(event.pos):
                    current_obstacles = generate_random_obstacles(start, goal, ROWS, COLS, NUM_OBSTACLES)
                    facts, agenda, parents, inference_chain, history, found, current_rule = reset(current_obstacles)

                elif def_rect.collidepoint(event.pos):
                    current_obstacles = set(DEFAULT_OBSTACLES)
                    facts, agenda, parents, inference_chain, history, found, current_rule = reset(current_obstacles)

        clock.tick(60)

if __name__ == "__main__":
    maze_solver_gmp_gui()
