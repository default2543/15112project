# Ultimate Tic-Tac-Toe

A playable Ultimate Tic-Tac-Toe game with a minimax AI opponent, built in Python
with `cmu_graphics` for CMU 15-112.

[Video demo](https://drive.google.com/file/d/141Kw-kuZQ4MVwWWrzOlswQ9otR-aD1Nn/view?usp=sharing)

## The game

The board is a 3×3 grid of smaller tic-tac-toe boards. The cell you play in
decides which small board your opponent must play on next. For example, a move
in the top-right cell of any small board sends your opponent to the top-right
board. If that board is already won or full, they may play anywhere.

Win a small board to claim that square on the big board. Win three small boards
in a row to win the game.

## Features

- **Single-player vs. AI** or local two-player mode
- **Minimax AI with alpha-beta pruning.** The heuristic scores won boards,
  control of the center and corner boards, and open strategic cells.
- **Optional move timer** (30 seconds per turn)
- In-game instructions and a demo screen

## Running it

Requires Python 3 and [`cmu_graphics`](https://academy.cs.cmu.edu/desktop).

```bash
pip install cmu-graphics
python3 temp.py
```

X moves first. In single-player mode, click the board after your move to
trigger the AI's reply.
