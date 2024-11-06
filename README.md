# Advanced Brick Breaker Game
An enhanced version of the classic brick breaker game developed using Python and Pygame, featuring power-ups, multiple levels, and dynamic gameplay.

## Features
1. Multiple Levels: Progress through increasingly challenging levels as you clear all bricks.
2. Power-Ups: Randomly dropping power-ups including paddle expansion, shrinking, ball speed adjustments.
3. Dynamic Score Display: Real-time score, lives, and level display.
4. Sound Effects: Interactive sound effects for paddle hits, brick breaking, and power-up collection.
   
## Requirements
1. Python 3.8+
2. Pygame library

## Installation
1. Clone the repository:
``` bash
git clone https://github.com/your-username/advanced-brick-breaker.git
cd advanced-brick-breaker
```

2. Install dependencies:
``` bash
pip install pygame
```

3. Add sound files:
Ensure the sound files hit.wav, break.wav, and powerup.wav are in the same directory as the code file.

4. Run the game:
``` bash
python brick_breaker.py
```

## Gameplay
Use the paddle to prevent the ball from falling off the screen, while aiming to break all the bricks.
Collect power-ups to gain advantages or overcome challenges.
Advance to the next level by clearing all bricks.

## Controls
Left Arrow Key: Move the paddle left
Right Arrow Key: Move the paddle right
Quit: Close the game window or press ESC

## Power-Ups
Power-ups drop randomly after breaking bricks:
*Expand: Increases paddle width.
*Shrink: Decreases paddle width.
*Slow: Slows down the ball speed.
*Fast: Speeds up the ball.

## Scoring and Levels
*Score: Earn 10 points for each brick broken.
*Levels: Clear all bricks to advance to the next level, which increases the ball speed.
*Lives: Start with 3 lives; lose one if the ball falls off the screen. Game over when all lives are lost.
