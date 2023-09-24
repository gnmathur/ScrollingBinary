"""
A program to display a scrolling binary stream in the terminal window like seen
in the movies. Each scrolling binary is color coded and the number of binary
digits in each column are random. The number of columns is determined by the
width of the terminal window. The scrolling speed is determined by the
SCROLL_SPEED constant. The busyness of the screen is determined by the BUSYNESS
constant. The higher the number, the more busy the screen.

Author: Gaurav Mathur
"""
import random
import shutil
import sys
import time
from typing import Tuple, Dict

# Get the size of the terminal window
TERM_WIDTH = shutil.get_terminal_size()[0]
# Scroll speed is the number of seconds to pause between printing the next frame
SCROLL_SPEED = 0.15
# Defines how busy the numbers appear on the screen. The more the number, the more busy the screen.
# Values range from 0 to 1, where 0 is no busy-ness (essentially blank
# screen :-)) and 1 is most busy. With 1, the screen will be completely filled with 0s or 1s
BUSYNESS = 0.02

term_clrs = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'reset': '\033[0m'
}

ColT = Dict[int, Tuple[str, int, str]]


def get_number_as_binary_string(num) -> str:
    """
    Returns the binary representation of a number as a string
    """
    bnum = ""
    while num > 0:
        bnum = str(num % 2) + bnum
        num = num // 2
    return bnum


def get_with_x_percent_prob(x) -> bool:
    """
    Returns True x percent of the time. x is a number between 0 and 100
    """
    return random.randint(1, 100) <= x


def get_random_color() -> str:
    """
    Returns a random color from the term_colors dict
    """
    return random.choice(list(term_clrs.keys())[:-1])


def update_map(col_map: ColT) -> ColT:
    """
    Updates the column map with a new binary number if the column is not in the map
    """
    for col in range(0, TERM_WIDTH):
        if col not in col_map:
            if get_with_x_percent_prob(BUSYNESS * 100):
                col_map[col] = \
                    (get_number_as_binary_string(random.randint(8, 2048)), 0, get_random_color())

    return col_map


if __name__ == "__main__":
    column_map: ColT = {}
    while True:
        column_map = update_map(column_map)
        for column in range(0, TERM_WIDTH):
            if column in column_map:
                bin_info = column_map[column]
                print(
                    f"{term_clrs[bin_info[2]]}{bin_info[0][bin_info[1]]}{term_clrs['reset']}",
                    end='')

                new_column = bin_info[1] + 1
                if new_column == len(bin_info[0]):
                    del column_map[column]
                else:
                    column_map[column] = (bin_info[0], new_column, bin_info[2])
            else:
                print(' ', end='')
        print()
        sys.stdout.flush()
        time.sleep(SCROLL_SPEED)
