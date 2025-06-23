
## Overview

This repository contains two implementations addressing the classic maze-solving problem using distinct paradigms in Artificial Intelligence:

1. **Forward Chaining with Generalized Modus Ponens (GMP)** — a logic-based, inference-driven approach that simulates knowledge-based reasoning.  
2. **Bidirectional Dijkstra Algorithm** — a graph-based shortest-path search utilizing simultaneous exploration from both source and goal states.

---

## 1. Forward Chaining Using Generalized Modus Ponens (GMP)
![image](https://github.com/user-attachments/assets/1599c34c-6e66-486e-8284-38cfa75ccef2)
![image](https://github.com/user-attachments/assets/e851e8af-805f-4849-8231-f12454a53759)
![image](https://github.com/user-attachments/assets/24336a07-eef9-451e-8cee-f132dd5023c0)
![image](https://github.com/user-attachments/assets/122e633d-dd2e-4370-9be0-4ac5413679ed)
![image](https://github.com/user-attachments/assets/72dcd89d-be7e-42d6-9b12-ae51596d9503)
![image](https://github.com/user-attachments/assets/7ff0cfb6-44ef-4d14-8d0e-6e196b915676)
![image](https://github.com/user-attachments/assets/f52053a5-6030-4f7f-9cf4-fa1ce39e37ce)



This system models the maze as a knowledge base and applies forward chaining with GMP to infer reachable states. The agent deduces its position solely through logical inference rules, without heuristics or goal orientation.

### Key Features
- **Fact Derivation**: Starts with `At(0,0)` and applies movement rules.
- **Rule Structure**: `At(x) ∧ CanMove(x, y) ⇒ At(y)`
- **Interactive Controls**: Step-by-step rule application and maze reset.
- **Visual Output**: Pygame GUI with grey cells for inferred states and purple lines for reasoning chains.

### Limitations
- No backtracking mechanism.
- Non-optimal due to exhaustive inference.
- Not goal-driven; exploration may expand irrelevant paths.

---

## 2. Bidirectional Dijkstra Algorithm

This implementation applies Dijkstra’s algorithm simultaneously from the start and goal nodes to efficiently discover the shortest path in the maze.

### Key Features
- **Dual Search**: Forward and backward frontiers expanded in parallel.
- **Meeting Point**: Path constructed upon frontier convergence.
- **Cost Function**: Uniform cost `g(n)` incremented per valid step.
- **Visualization**:
  - Start: Green
  - Goal: Red
  - Obstacles: Black
  - Forward Visited: Light Blue
  - Backward Visited: Light Pink
  - Meeting Node: Gold
  - Final Path: Blue

---

## Dependencies

- Python 3.10+
- [Pygame](https://www.pygame.org/) for visualization

```bash
pip install pygame
