import os
from copy import deepcopy
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

    def __init__(self, input_map, current_pos, current_direction):
        self.define_inv_direction_map()
        self.input_map = input_map 
        self.map_size = len(self.input_map), len(self.input_map[0])
        self.current_pos, self.direction = current_pos, current_direction
        self.position_history = [self.current_pos]
        self.direction_history = [self.direction] 
        self.obstacle_locations = []

    def show_map(self):
        for line in self.input_map:
            print(line)

    @classmethod
    def get_initial_conditions(cls, input_map): 
        for row_idx in range(len(input_map)):
            for col_idx in range(len(input_map[0])):
                if input_map[row_idx][col_idx] in cls.direction_map.keys(): 
                    return (row_idx, col_idx), cls.direction_map[input_map[row_idx][col_idx]]

        return None

    def rotate(self, direction):
        #print(f"Changing directions from {self.direction}")
        return (direction[1], direction[0] * -1)

    def get_next_pos(self, current_pos, direction):
         return (current_pos[0] + direction[0], current_pos[1] + direction[1]) 

    def is_obstacle(self, pos):
        if self.input_map[pos[0]][pos[1]] == '#':
            return True
        else:
            return False

    def is_oob(self, pos):
        if pos[0] >= self.map_size[0] or pos[0] < 0:
            return True 
        elif pos[1] >= self.map_size[1] or pos[1] < 0:
            return True 
        else:
            return False

    def deja_vu(self):
        for p, d in zip(self.position_history, self.direction_history):
            if self.current_pos == p and self.direction == d:
                return True
        return False

    def move(self):
        if self.check_for_loop:
            self.check_for_loop()

        candidate_pos = self.get_next_pos(self.current_pos, self.direction)

        #print(f"Checking if we can use {candidate_pos} going in direction {self.direction}")

        if self.is_oob(candidate_pos):
             return None 
        elif self.is_obstacle(candidate_pos):
             self.direction = self.rotate(self.direction)
             return self.move()
        else:
            self.current_pos = candidate_pos

        self.position_history.append(self.current_pos)
        self.direction_history.append(self.direction)

        # Draw obstacle logic
        if self.input_map[self.current_pos[0]][self.current_pos[1]] != "O":
            self.input_map[self.current_pos[0]][self.current_pos[1]] = self.inv_direction_map[self.direction]

        if self.deja_vu():
            return  

        return self.current_pos

    def check_for_loop(self):
        obs_loc = self.get_next_pos(self.current_pos, self.direction)
        if not self.is_oob(obs_loc) and not self.is_obstacle(obs_loc):
            _mapnav = MapNavigator(deepcopy(self.input_map), self.current_pos, self.rotate(self.direction))
            _mapnav.position_history = deepcopy(self.position_history)
            _mapnav.direction_history = deepcopy(self.direction_history)
            _mapnav.check_for_loop = False
            loop_found = False
            while not loop_found:
                print("Checking da loop!")
                if _mapnav.__next__() == "Loop":
                    #print(f"Adding {obs_loc} to candidate list of obstacles from {self.current_pos}")
                    self.input_map[obs_loc[0]][obs_loc[1]] = "0"
                    self.obstacle_locations.append(obs_loc)
                    print("loop found, man!")
                    loop_found = True

            del _mapnav

    def __iter__(self):
        return self

    def __next__(self):
       next_move = self.move()
       if next_move is not None:
          return next_move
       raise StopIteration

    def show_current_map(self):
       sample_map = self.input_map
       window_size = 20

       for r in sample_map[max(0, self.current_pos[0] - window_size):min(self.current_pos[0] + window_size, self.map_size[0])]:
           for c in r:
               if c == '#':
                   print_yellow(c, end="")
               elif c in self.direction_map.keys():
                   print_red(c, end="")
               elif c == "O": 
                   print_blue(c, end="")
               else:
                   print_dark_gray(c, end="")
           print("")

clear_screen()

input_map = []
with open(sys.argv[1]) as f:
    for line in f:
        input_map.append(list(line.replace('\n', '')))

init_pos, init_dir = MapNavigator.get_initial_conditions(input_map)

test_map = MapNavigator(input_map, init_pos, init_dir)

def screen_refresh_func(sleep_time):
    if sleep_time > 10:
        return clear_screen
    else:
        return move_cursor_to_top

screen_refresh = screen_refresh_func(float(sys.argv[2]))

for p in test_map: 
    screen_refresh()
    print(sys.argv[1])
    print("I'm trying to show tha map!!!")
    test_map.show_current_map()
    unique_pos = set(test_map.position_history)
    print(f"""
    Num unique positions: {len(unique_pos)} 
    Num Total Positions: {len(test_map.position_history)} 
    Num Repeated Pos. {len(test_map.position_history) - len(unique_pos)} 
    Perc. of Unique = {round(len(unique_pos) / len(test_map.position_history), 2)} 
    Num. Obstacle Locations = {len(test_map.obstacle_locations)}""")
    print(f"Position history: {test_map.position_history}")
    sleep(float(sys.argv[2]))

