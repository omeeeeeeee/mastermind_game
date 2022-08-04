# Installation
This project requires Python 3.8 or greater. To run, just copy the directory to your local machine by downloading the 
source 
code or cloning the repository. Navigate to 
the root directory of the program and install the requirements needed.
```
pip install -r requirements.txt
```
To start the game, just run `main.py` using Python 3.
```
python main.py
```
If the coloured texts aren't rendering properly, try compiling the program as a single executable. I found that 
`pyinstaller` works well for this:
```
pip install pyinstaller
pyinstaller --onefile main.py
```
The executable should be found in the `dist` folder. If you encounter permission errors, move `main.py` to a 
different folder and re-run the script in that directory.

# Gameplay Specifications
## Classic Rules
The classic version of Mastermind can be played online [here](https://webgamesonline.com/mastermind/) and the general rules can be found [here]( https://webgamesonline.com/mastermind/rules.php).

## Specifications
For our CS11 MP2 class, there are specific modifications to the game that we have to follow. Namely,

- The game will be a console-based text game.
- Instead of colours for code pegs, use numbers (`0-9`).
- Use `R` (correct colour, correct position) and `W` (correct colour, wrong position) to represent key pegs.
- For each game, the CPU will randomly generate a pattern of length ranging from `4` to `8`. The code can contain 
  duplicates.
- Players will have "lifelines" which they can use for a guess attempt.

### Lifelines

Every guess attempt, a player can ask for a lifeline. They may only ask once for the whole duration of the game.

There are two types of lifelines.
- `lifeline#1` - Reveal a colour in the generated code. Using this lifeline decreases guesses by `1`.
- `lifeline#2` - Reveal a correct colour in one position. Using this lifeline decreases guesses by `2`.

## Basic Game Example
```
Hidden code is of length 6.
Total number of Guesses: 10

Guess #1
Enter guess> 203045
2R - 3W

Guess #2
Enter guess> lifeline#2
Hidden code contains digit 3 at position 4
Note: Total number of guesses is reduced by 2.

Guess #2
Enter guess> 023345
5R - 0W

Guess #3
Enter guess> 022345
YOU WIN!!
```