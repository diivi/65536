# AI Solver using Monte Carlo Tree Search (MCTS) for 2048

## Overview

The AI agent for 2048 is implemented using the Monte Carlo Tree Search algorithm. This solver aims to make informed decisions about the best move in a given game state by simulating multiple random games and choosing the move that leads to the highest overall score.

## Components

### 1. Random Policy

- The `random_policy` function simulates random moves in a given game until a game-over state is reached.
- The score and the maximum tile value achieved in the simulated games are recorded.

### 2. MCTS (Monte Carlo Tree Search)

- The `mcts` function performs Monte Carlo Tree Search for each possible move (up, down, left, right).
- It utilizes the `random_policy` to simulate multiple games and accumulate scores for each move.
- The move with the highest accumulated score is selected as the best move.

### 3. Monte Carlo Simulation

- The `monte_carlo_simulation` function applies the MCTS algorithm iteratively until a game-over state is reached.
- It prints the final state of the game, the total score, and the maximum tile value achieved.

### Monte Carlo Tree Search (MCTS)
**Monte Carlo Tree Search (MCTS) Overview**

Monte Carlo Tree Search (MCTS) is a popular algorithm used in decision-making processes, particularly in artificial intelligence for games and optimization problems. It is commonly employed when the full state space is too vast to explore exhaustively.

### Key Concepts:

1. **Tree Search:**
   - MCTS builds a tree structure representing possible sequences of moves in a game or actions in a decision-making scenario.

2. **Monte Carlo Simulation:**
   - The algorithm relies on random sampling (Monte Carlo simulations) to explore parts of the decision space, gradually refining its understanding of the most promising choices.

3. **Four Key Steps:**
   - **Selection:** Starting from the root of the tree, traverse down the tree based on certain criteria (often using UCT - Upper Confidence Bounds for Trees) to find a promising node.
   - **Expansion:** Expand the selected node by adding one or more child nodes representing possible moves or actions.
   - **Simulation:** Conduct a Monte Carlo simulation from the newly added node. This involves making random moves or decisions until a terminal state is reached.
   - **Backpropagation:** Update the statistics (e.g., visit count, total reward) of the nodes visited during the simulation. Propagate this information up the tree.

### MCTS in the Context of 2048 Solver:

- **Selection:** The algorithm selects moves (up, down, left, right) based on accumulated statistics, favoring moves that lead to higher scores in the simulations.
  
- **Expansion:** For each selected move, the algorithm explores possible outcomes by adding child nodes representing different game states.

- **Simulation:** The `random_policy` function simulates multiple random games from each newly added node to estimate the potential outcomes of the move.

- **Backpropagation:** The results of the simulations are used to update the statistics of the nodes visited during the selection and expansion steps.

### Purpose in 2048 Solver:

- **Optimal Move Selection:** MCTS helps the AI make informed decisions on the best move in a given game state.
  
- **Dynamic Decision Making:** By using random simulations, the algorithm adapts to the dynamic nature of the game, providing a balance between exploration and exploitation.

- **Efficient Exploration:** Instead of exhaustively searching the entire decision space, MCTS focuses on promising regions, making it suitable for scenarios with large and uncertain state spaces.

In the provided 2048 solver, MCTS is applied iteratively to determine the best move that maximizes the overall score based on the outcomes of simulated games.


## Notes

- Adjust the number of iterations in the `random_policy` function based on computational resources and desired accuracy.
- The code assumes the existence of the `Game` class with the `move`, `check_game_over`, and other relevant methods.

50 Rollouts and 25 games

| Heuristic                                  | 1024 Probability | 2048 Probability | 4096 probability | Average Score | Max Score | Average Time |
| ------------------------------------------ | ---------------- | ---------------- | ---------------- | ------------- | --------- | ------------ |
| Maximum Monotonicity                       | 0                | 0                | 0                | 512           | 960       | 33 seconds   |
| Maximum Score per Round                    | 0.12             | 0                | 0                | 5312          | 15164     | 61 seconds   |
| Average Mergability                        | 0.24             | 0                | 0                | 5974          | 14044     | 52 seconds   |
| Sum of Scores and Tile Values per Round    | 0.88             | 0.48             | 0                | 21368         | 35272     | 94 seconds   |
| Sum of Scores per Round                    | 0.92             | 0.56             | 0.04             | 24798         | 65656     | 200 seconds  |
| Sum of Scores with priority to up and left | 0.96             | 0.72             | 0.04             | 26407         | 51136     | 115 seconds  |
