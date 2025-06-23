
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

### Random Maze
![image](https://github.com/user-attachments/assets/0a154d26-8f50-4941-830f-7d84bec832bd)

### Limitations
- No backtracking mechanism.
- Non-optimal due to exhaustive inference.
- Not goal-driven; exploration may expand irrelevant paths.

---

## 2. Bidirectional Dijkstra Algorithm

This implementation applies Dijkstra’s algorithm simultaneously from the start and goal nodes to efficiently discover the shortest path in the maze.

![image](https://github.com/user-attachments/assets/9a49ed38-2742-4dc9-ae1d-52ec524fa616)
![image](https://github.com/user-attachments/assets/7aa30bc1-08d1-4022-b99a-1586c8c8b9ff)
![image](https://github.com/user-attachments/assets/b8b5b055-c2ac-4edf-9be8-b9d0e468fecc)
![image](https://github.com/user-attachments/assets/5bcce4a7-3b41-482d-8b2c-d58608391540)
![image](https://github.com/user-attachments/assets/026734bb-72d3-4b1b-88c3-e9d167ee4a84)
![image](https://github.com/user-attachments/assets/bd8a114a-f4ae-4a4e-b8c4-8f7f9ff1ea16)
![image](https://github.com/user-attachments/assets/baf2484b-deef-48bf-b6e7-dba760a619b3)
![image](https://github.com/user-attachments/assets/7f8cdcb4-1ade-40ba-8e09-4c7c9080df31)
![image](https://github.com/user-attachments/assets/da772588-6251-48fe-be45-2b84bf427d10)

### Random Maze
![image](https://github.com/user-attachments/assets/14618498-8305-4f22-8097-3c03f27bcffc)
![image](https://github.com/user-attachments/assets/28f55fc1-9cf5-4aa6-a000-5476cfa81ba4)


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
