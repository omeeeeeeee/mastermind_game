"""
  __  __           _                      _           _
 |  \/  |         | |                    (_)         | |
 | \  / | __ _ ___| |_ ___ _ __ _ __ ___  _ _ __   __| |
 | |\/| |/ _` / __| __/ _ \ '__| '_ ` _ \| | '_ \ / _` |
 | |  | | (_| \__ \ ||  __/ |  | | | | | | | | | | (_| |
 |_|  |_|\__,_|___/\__\___|_|  |_| |_| |_|_|_| |_|\__,_|

Group Members
2021 02371 - Marius Barcenas
2021 04971 - Naomi Amparo
2021 10776 - Jakin Bacalla
"""

from random import randint, choice
from typing import Tuple
from colorama import init

# Constants
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

DIFFICULTY = {
    4: f"{OKGREEN}VERY EASY{ENDC}",
    5: f"{OKGREEN}EASY{ENDC}",
    6: f"{WARNING}AVERAGE{ENDC}",
    7: f"{FAIL}HARD{ENDC}",
    8: f"{FAIL}VERY HARD{ENDC}"
}


def generate_pattern(length: int) -> str:
    """ Generates a random pattern of digits of a specified length.

    :param length: Length of pattern to generate.
    :return: String of digits.
    """
    if length < 0:
        raise ValueError("Pattern `length` must be a positive integer. Given: {}".format(length))

    digits = []

    for i in range(length):
        digits += [str(randint(0, 9))]

    return ''.join(digits)


def compare_guess(guess: str, pattern: str) -> Tuple[bool, bool, str]:
    """Compares the guess with the pattern and return

    :param guess: The player's guess.
    :param pattern: The correct pattern.
    :return: A tuple containing whether the player has won, if they consumed a guess, and the status message.
    """
    length = len(pattern)

    # Guard closes against invalid inputs
    if guess in ['lifeline#1', 'lifeline#2']:
        return False, False, "Need help?"

    if not guess.isdigit():
        return False, False, "Invalid guess! The guess must consist only of digits or lifelines."

    if len(guess) != length:
        return False, False, f"Incorrect guess length! The pattern length is {length} (received: {len(guess)})"

    if guess == pattern:
        return True, True, "YOU WON"

    # Logic to determine how many R and W if the guess is valid but incorrect
    guess_list = list(guess)
    pattern_list = list(pattern)

    correct_place = 0
    correct_colour = 0

    # Compares the guess with the pattern starting from the end to count R
    for i in reversed(range(length)):
        if guess[i] == pattern[i]:
            correct_place += 1
            guess_list.pop(i)
            pattern_list.pop(i)

    # Counts how many of the remaining digits in the guess are in the pattern for W
    for item in guess_list:
        if item in pattern_list:
            correct_colour += 1
            pattern_list.remove(item)

    return False, True, f"{correct_place}R - {correct_colour}W"


def draw_board(guesses: list[tuple], max_guesses: int, length: int) -> None:
    """
    Draws the board

    :param guesses: list containing a tuple of previous guesses as well as statuses
    :param max_guesses: the number of guesses the player is allowed
    :param length: length of the pattern
    :return: None
    """
    VERT = f"{OKBLUE}║{ENDC}"

    print(f"{OKBLUE}╔════╦═{'═' * max(5, length * 2 - 1)}═╦═════════╗{ENDC}")
    print(f"{OKBLUE}║ ## ║ Guess{' ' * max(0, length * 2 - 6)} ║ Status  ║{ENDC}")
    print(f"{OKBLUE}╠════╬═{'═' * max(5, length * 2 - 1)}═╬═════════╣{ENDC}")

    for i in range(max_guesses):
        if i < len(guesses):
            print(f"{VERT} {str(i + 1).rjust(2)} {VERT} {guesses[i][0]} {VERT} {guesses[i][1]} {VERT}")
        else:
            print(f"{VERT} {str(i + 1).rjust(2)} {VERT} {'_ ' * (length - 1)}_ {VERT}         {VERT} ")

    print(f"{OKBLUE}╚════╩═{'═' * max(5, length * 2 - 1)}═╩═════════╝{ENDC}")


def start_game(**kwargs) -> None:
    """Starts the program.

    :key pattern_length: (``int``) Length of the pattern to be guessed. Default is a random integer from `4-8`.
    :key max_guesses: (``int``) Amount of allowable guesses by the player. Default is 10.
    :return: None
    """

    # Generate pattern
    pattern_length = kwargs.get('pattern_length', randint(4, 8))
    max_guesses = kwargs.get('max_guesses', 10)
    pattern = generate_pattern(pattern_length)
    pattern_list = list(pattern)

    # Initialise game variables
    guesses = []
    guess_count = 1
    lifeline_count = 0
    is_playing = True

    # Start the game cycles

    print(f"{BOLD}{UNDERLINE}GAME START{ENDC}")
    print(f"{BOLD}Are you truly the master of your mind?{ENDC}")
    print(f"{BOLD}Difficulty: {DIFFICULTY[pattern_length]}{ENDC}")
    print(f"{BOLD}Hidden code is of length {OKCYAN}{pattern_length}{ENDC}")
    print(f"{BOLD}Total number of guesses: {OKCYAN}{max_guesses}{ENDC}")

    while is_playing:
        print()
        print(f"{UNDERLINE}Guess #{guess_count}{ENDC}")
        guess = input("Enter guess > ").lower().replace(" ", "")

        has_won, consumed_guess, status = compare_guess(guess, pattern)

        # Increments guess count and draws the board if player uses a valid guess
        # Prints the status otherwise
        if consumed_guess:
            guesses += [(" ".join(list(guess)), status)]
            guess_count += 1
            draw_board(guesses, max_guesses, pattern_length)
        else:
            print(f"{FAIL}{status}{ENDC}")

        # Win or lose logic
        if has_won:
            print("YOU WIN!!")
            is_playing = False
        elif guess_count >= max_guesses:
            print("YOU LOST!!")
            print(f"The code is {pattern}")
            is_playing = False

        # Display hints when user asks for a lifeline. Lifelines can only be used once.
        if guess == 'lifeline#1':
            lifeline_count += 1

            if guess_count < 9:
                if lifeline_count == 1:
                    max_guesses -= 1

                    digit_hint = choice(pattern_list)

                    print(f"Hidden code contains digit {digit_hint}.")
                    print("Note: Total number of guesses is reduced by 1.")

                else:
                    print("Sneaky. You can only use lifelines once!")
            else:
                print("Sorry. You can't use lifeline#1 anymore!")
        elif guess == 'lifeline#2':
            lifeline_count += 1

            if guess_count < 8:
                if lifeline_count == 1:
                    max_guesses -= 2

                    digit_hint = choice(pattern_list)
                    digit_pos = pattern_list.index(digit_hint) + 1

                    print(f"Hidden code contains digit {digit_hint} at location {digit_pos}.")
                    print("Note: Total number of guesses is reduced by 2.")
                else:
                    print("Sneaky. You can only use lifelines once!")
            else:
                print("Sorry. You can't use lifeline#2 anymore!")


if __name__ == "__main__":
    init()

    print(f"""If you see weird stuff like '←[95m', please use a
different terminal or this will not be a good experience.
{HEADER}
  __  __           _                      _           _
 |  \/  |         | |                    (_)         | |
 | \  / | __ _ ___| |_ ___ _ __ _ __ ___  _ _ __   __| |
 | |\/| |/ _` / __| __/ _ \\ '__| '_ ` _ \| | '_ \ / _` |
 | |  | | (_| \__ \ ||  __/ |  | | | | | | | | | | (_| |
 |_|  |_|\__,_|___/\__\___|_|  |_| |_| |_|_|_| |_|\__,_|
{ENDC}{OKGREEN}
 HOW TO PLAY
 (1) A pattern of digits [0-9] will be randomly generated.
 (2) Your goal is to guess the pattern within 10 tries.
 (3) You may use lifelines but they will reduce the number
     of tries that you have.
     (-) lifeline#1 - Give a correct digit; reduces the
         number of tries by 1
     (-) lifeline#2 - Give a correct digit at the correct
         location; reduces the number of tries by 2
 (4) The difficulty of each round is randomly selected and
     will affect the pattern length.
     (-) The ability to set the difficulty is a paid DLC /s
 (5) The game ends when the pattern is guessed or the max
     amount of tries is reached.
{ENDC}""")

    while True:
        start_game()
        restart = input("Restart the game? [Yes or No]").lower().replace(" ", "")
        if restart == 'no':
            quit()


"""
   _
._(.)< (quack quack)
 \__)
~~~~~~~~~~~~~~~~~~~~
"""