from copy import deepcopy
import os
from time import sleep
import sys

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def move_cursor_to_top():
    print("\033[H", end="") 

def print_red(text, end="\n"):
    print(f"\033[1;31m{text}\033[0m", end=end)  # Bright Red


def print_green(text, end="\n"):
    print(f"\033[1;32m{text}\033[0m", end=end)  # Bright Green


def print_blue(text, end="\n"):
    print(f"\033[1;34m{text}\033[0m", end=end)  # Bright Blue


def print_yellow(text, end="\n"):
    print(f"\033[1;33m{text}\033[0m", end=end)  # Bright Yellow


def print_dark_gray(text, end="\n"):
    print(f"\033[1;90m{text}\033[0m", end=end)

class MapNavigator:
    direction_map = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0)
        }

    def define_inv_direction_map(self):
        self.inv_direction_map = {
            v: k for k, v in self.direction_map.items()
        }

    def __init__(self, map_filepath):
        self.define_inv_direction_map()
        self.input_map = []

        with open(map_filepath) as f:
            for line in f:
                self.input_map.append(list(line.replace('\n', '')))

        self.map_size = len(self.input_map), len(self.input_map[0])
        self.current_pos, self.direction = self.get_initial_conditions()
        self.position_history = [tuple(self.current_pos)]
        self.input_map[self.current_pos[0]][self.current_pos[1]] = '.'

    def show_map(self):
        for line in self.input_map:
            print(line)

    def get_initial_conditions(self): 
        for row_idx in range(len(self.input_map)):
            for col_idx in range(len(self.input_map[0])):
                if self.input_map[row_idx][col_idx] in self.direction_map.keys(): 
                    return (row_idx, col_idx), self.direction_map[self.input_map[row_idx][col_idx]]

        return None

    def rotate_direction(self):
        #print(f"Changing directions from {self.direction}")
        return self.direction[1], self.direction[0] * -1

    def get_next_pos(self):
         return [self.current_pos[0] + self.direction[0], self.current_pos[1] + self.direction[1]] 

    def peek(self):
        next_pos = self.get_next_pos() 
        if next_pos[0] >= self.map_size[0] or next_pos[0] < 0:
            return None
        elif next_pos[1] >= self.map_size[1] or next_pos[1] < 0:
            return None
        else:
            return self.input_map[next_pos[0]][next_pos[1]]

    def move(self):
        next_pos = self.get_next_pos()
        if next_pos[0] >= self.map_size[0] or next_pos[0] < 0:
            #print(f"going OOB at {next_pos}")
            return None
        elif next_pos[1] >= self.map_size[1] or next_pos[1] < 0:
            #print(f"going OOB at {next_pos}")
            return None
        else:
            if self.peek() != '#':
                self.current_pos = next_pos
                self.position_history.append(tuple(self.current_pos))
                return self.current_pos
            else:
                self.direction = self.rotate_direction()
                return self.move()

    def __iter__(self):
        return self

    def __next__(self):
       next_move = self.move()
       if next_move is not None:
           return next_move
       raise StopIteration

    def show_current_map(self):
       sample_map = self.input_map
       direction_char = self.inv_direction_map[tuple(self.direction)]
       #print(f"Printing pos {(self.current_pos[0], self.current_pos[1])}")
       sample_map[self.current_pos[0]][self.current_pos[1]] = direction_char

       window_size = 20

       for r in sample_map[max(0, self.current_pos[0] - window_size):min(self.current_pos[0] + window_size, self.map_size[0])]:
           for c in r:
               if c == '#':
                   print_yellow(c, end="")
               elif c in self.direction_map.keys():
                   print_red(c, end="")
               else:
                   print_dark_gray(c, end="")
           print("")


test_map = MapNavigator(sys.argv[1])

for p in test_map: 
    clear_screen()
    print(sys.argv[1])
    test_map.show_current_map()
    unique_pos = set(test_map.position_history)
    print(f"Num unique positions: {len(unique_pos)} // Num Total Positions: {len(test_map.position_history)} // Num Repeated Pos. {len(test_map.position_history) - len(unique_pos)} // Perc. of Unique = {round(len(unique_pos) / len(test_map.position_history), 2)}")
    sys.stdout.flush()
    sleep(float(sys.argv[2]))


