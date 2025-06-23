# CS6053 Artificial Intelligence and Machine Learning  
### Group Project: Maze Solving via Logic Inference and Bidirectional Search  

**Author:** Bajram Visha  
**Student ID:** 21045442  
**Module Leader:** Vassil Vassilev  

---

## Overview

This repository contains two implementations addressing the classic maze-solving problem using distinct paradigms in Artificial Intelligence:

1. **Forward Chaining with Generalized Modus Ponens (GMP)** — a logic-based, inference-driven approach that simulates knowledge-based reasoning.  
2. **Bidirectional Dijkstra Algorithm** — a graph-based shortest-path search utilizing simultaneous exploration from both source and goal states.

---

## 1. Forward Chaining Using Generalized Modus Ponens (GMP)

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
