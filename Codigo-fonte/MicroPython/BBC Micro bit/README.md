# BBC Micro:bit MicroPython practices

Public repository for practices and postings of micropython codes for BBC Micro: bit boards.

## Codes
Summary of codes :

#### 1. Game codes

1.1. [Le-ght](https://github.com/EduardoDestefani/micropython-samples/blob/master/Codigo-fonte/MicroPython/BBC%20Micro%20bit/Le-ght.py) (a left and right game) ; it is a game based on micropython that consists of reflexes. 

- Operation :

  - The player must choose the difficulty (level 1 to 4, are alternated by pressing button B);
  - To confirm the option of difficulty, press button A and wait for the instructions on the screen;
  - Prepare for the instructions that will appear on the BBC Micro:bit's 25 LED screen;
  - The instructions are; left or right, displayed through an arrow that points to button B (right) or button A (left);
  - The player must press the button that refers to the indicated direction;
  - With each hit, the arrow is shown less time on the screen (randomly), if the player misses, the game restarts and shows the amount of points achieved;
  - If he reaches the number of points that the difficulty level asks for, he wins the game (difficulty equal to 4 requires 20 points to win, equal to 3, 15 points, equal to 2, 12 points and equal to 1, 10 points).

1.2. [D-Bit](https://github.com/EduardoDestefani/micropython-samples/blob/master/Codigo-fonte/MicroPython/BBC%20Micro%20bit/D-Bit.py) (a RPG dice for BBC Micro:bit) ; it is a micropython software that simulates RPG dice.

- Operation :

  - The player must select the type of dice, being them ; D2, D4, D6, D8, D10, D20 and D100;
  - To select, he must choose the option for each dice, for example (D2 = option 1, D4 = option 2, ... D100 = option 7);
  - The options (from 1 to 7, D2 to D100), are alternated by pressing button B. To confirm the option, press button A and wait for the "Shake" instruction on the screen;
  - After the instruction displayed on the screen, swing the BBC Micro: bit and wait for the result;
  - If you want to play again, press button A to restart the software.
