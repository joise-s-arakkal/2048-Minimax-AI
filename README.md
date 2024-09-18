# 2048 with Minimax AI

A modern and enhanced version of the classic 2048 puzzle game built using Python and Pygame. The game also features a smart AI powered by the Minimax algorithm with Alpha-Beta Pruning, allowing the AI to play the game with high efficiency.

## Features

- **AI Integration:** AI helper using the Minimax algorithm and Alpha-Beta pruning.
- **Smooth Gameplay:** Responsive and fluid gameplay with intuitive keyboard controls.
- **Score Tracking:** Keeps track of your score, with real-time updates during gameplay.
- **Retry Option:** Retry the game from scratch when the board is full and no moves are possible.
- **Real-time Rendering:** Tiles and score update dynamically with every move.

## Gameplay

- **Objective:** combine tiles with the same numbers to create larger tiles and reach the 2048 tile or beyond.
- **Controls:** 
    - **Arrow Keys:** Move tiles up, down, left, or right.
    - **'A' Key:** Let the AI take the next move.


## Requirements

- Python 3.x
- Pygame library

You can install Pygame using pip:

```bash
pip install pygame
```

## Gameplay Video

![Gameplay](https://github.com/joise-s-arakkal/2048-Minimax-AI/blob/main/game_play.gif)


## How the AI Works

The AI utilizes the Minimax algorithm with Alpha-Beta pruning to decide the best possible move based on:

- **Empty Tiles:** Prioritizing open spaces to maximize move potential.
- **Tile Merging Potential:** Looking for opportunities to merge large tiles.
- **Monotonicity:** Encouraging gradual increase of tile values.
- **Weighted Grid:** Focusing on placing larger tiles in favorable positions (such as corners).

## License 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License. See the [LICENSE](https://github.com/joise-s-arakkal/2048-Minimax-AI/blob/main/LICENSE) file for details.
