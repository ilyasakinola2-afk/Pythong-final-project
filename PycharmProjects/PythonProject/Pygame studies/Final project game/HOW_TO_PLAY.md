# Tank Shooters

## Run

From this folder, run:

```powershell
python finalproject.py
```

Pygame must be installed in the Python environment used to run the game.

## Menu

- Choose **2 Players** or **Player vs Bot** with the mouse, or press `1` or `2`.
- Press `M` to toggle the synthesized background music.
- Press `F11` to toggle fullscreen.
- Press `Esc` to quit from the menu.

## Controls

- Player 1: `W A S D` to move and face; hold `Space` to fire.
- Player 2: arrow keys to move and face; hold `Enter` to fire.
- During a match, `Esc` returns to the menu.
- After a match, `R` starts a rematch and `M` returns to the menu.

## Pickups

- `S`: blocks one hit for five seconds.
- `2`: doubles movement speed for five seconds.
- `R`: increases firing speed for five seconds.

Tanks have three health points by default so the health bars are useful. Change `MAX_HEALTH` near the top of `finalproject.py` to `1` for one-hit kills.

The game uses the Kenney tank pack in `assets/`; its included license allows personal and commercial use (CC0).
