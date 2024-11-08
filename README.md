
GAME DESCRIPTION
The game features a paddle, a ball, and a destructible wall of blocks. The goal is to bounce the ball off the paddle and break all the blocks. The game ends when the ball falls below the paddle.

MAIN CONCEPTS

Wall of Blocks: The blocks are arranged in a grid and have varying strengths. The blocks' colors change depending on their strength.
Paddle Control: The player controls the paddle using the left and right arrow keys.
Ball Movement: The ball bounces off the paddle and walls. If the ball hits a block, the block's strength reduces.
Game Over / Win Conditions: The game ends when the ball falls below the paddle or when all blocks are destroyed.
Start Game: The player can click anywhere to start the game after a win or loss.


MACHINE REQUIREMENTS AND INSTRUCTIONS
-  install Python 3.x
- install Pygame library

1. Install Python 3 if you don't already have it.
2. Install the Pygame library:
    `bash
    pip install pygame
    ```

INSTRUCTIONS OF THE GAME
- Use the left or right arrow keys to move the paddle.
- The goal is to destroy all the blocks by bouncing the ball off the paddle.
- If the ball falls below the paddle, you lose the game.
- If all blocks are destroyed, you win the game.

Code Breakdown
-wall class: Defines the blocks in the game, including their position, strength, and color. Blocks are destroyed when hit by the ball.
paddle class: Controls the paddle's position and movement using the keyboard (left and right arrows).
-game_ball class: Controls the ball’s movement, collision detection, and interaction with the paddle and blocks. The ball bounces off surfaces and changes its direction accordingly.
-Main Game Loop: The game runs inside a while loop where objects are drawn, movements are updated, and collisions are checked every frame.

 How to Start AND ENJOY THE GAME

1. After running the game, click the right or left pad on the screen to start.
2. Use the arrow keys to move the paddle and break all the blocks.
3. When all blocks are destroyed, you win! If the ball falls off the screen, you lose.

