<h1 align="center">🔍 Search Algorithms Repository</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8.5-blue" alt="Python 3.8.5">
</p>

<p>
  This repository contains implementations of search algorithms in Python, developed as part of my studies in Artificial Intelligence.
</p>

---

## 📚 About Uninformed Search Algorithms

Uninformed search algorithms (also called blind search algorithms) explore a problem space without any additional information about the goal's location. They systematically traverse the search space to find a solution but do not use heuristics or domain-specific knowledge.

### Implemented algorithms:

- **Depth-First Search (DFS)**  
  Explores as far as possible along one branch before backtracking. It's memory-efficient but may not find the optimal solution.

- **Breadth-First Search (BFS)**  
  Explores all the nodes at the current depth level before moving on to the next. It guarantees the shortest path in terms of steps when step costs are equal.

- **Greedy Best-First Search (GBFS)**
  Explores the nodes that are closest to the goal based on a heuristic function. It's memory-efficient but may not find the optimal solution.

These algorithms are commonly used in:
- Maze solving
- Puzzle solving
- Simple games
- Decision tree exploration

---

## 🛠️ Requirements

- Python 3.8.5 or later

---

## 🚀 How to Run

Clone the repository:

```bash
git clone https://github.com/kaikyMoura/UninformedSearch-algorithms.git
cd UninformedSearch-algorithms
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Then run one of the scripts, for example:
```bash
python maze.py maze1.tsx
```

The script will read the maze from the file and solve it using the specified uninformed search algorithm.

> ⚠️ **Important**
> </br> To change algorithm, modify the `method` variable in the end of the script.

---

## 🎓 Purpose
This repository was created as part of my learning journey in Artificial Intelligence, inspired by the CS50’s Introduction to AI with Python course by Harvard University.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
