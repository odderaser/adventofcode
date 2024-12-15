import sys
from functools import cmp_to_key

def parse_input(filename):
    pmap = []
    with open(filename) as f:
        for line in f:
            pmap.append(list(line.replace('\n', '')))

    return pmap, (len(pmap), len(pmap[0]))

class Map:

    def __init__(self, filename):
        self.pmap = []
        with open(filename) as f:
            for line in f:
                self.pmap.append(list(line.replace('\n', '')))

        self.map_size = (len(self.pmap), len(self.pmap[0]))

    def oob(self, pos):
        for idx in range(len(pos)):
            if pos[idx] < 0 or pos[idx] >= self.map_size[idx]:
                return True

        return False

    def __getitem__(self, index):
        return self.pmap[index[0]][index[1]] 
        
    def show_map(self):
        for line in self.pmap:
            for c in line:
                print(c, end="")
            print("")

def add(pos, vec):
    res = [0, 0]
    for idx in range(len(pos)):
        res[idx] = pos[idx] + vec[idx]

    return tuple(res)

def adjacent(pos1, pos2):
    for pdir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if add(pos1, pdir) == pos2:
            return True
    return False

def find_regions(pmap):
   
    stack = [(0,0)]
    visited = set()
    regions = []

    while len(stack) > 0:

        pos = stack.pop()

        # Step 1: find adjacent squares and add to the stack
        _stack = []
        for pdir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ppos = add(pos, pdir)
            if not pmap.oob(ppos) and ppos not in visited and ppos not in stack:
                _stack.append(ppos)

        def _cmp_fn(a, b):
            print(a, b)
            if pmap[a] == pmap[pos]:
                return False 
            elif pmap[b] == pmap[pos]: 
                return True
            else:
                return True
            
        print(_stack)
        stack.extend(_stack.sort(key=cmp_to_key(_cmp_fn)))
        visited.add(pos)

        # Step 2: Is the current position part of an existing region?
        added = False
        for ridx in range(len(regions)):
            for rpos in regions[ridx]:
                if adjacent(pos, rpos) and pmap[pos] == pmap[rpos]:
                    regions[ridx].append(pos)
                    added = True

        if not added:
            print(f"Creating a new region for {pmap[pos]}")
            regions.append([pos])
                    
    return regions

def traverse(region):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    current_dir_idx = 0
    history = [region[0]]
    dir_history = [dirs[current_dir_idx]]
    complete_cycle = False
    cycle_start_idx = -1
    pos = region[0]

    while not complete_cycle:
        next_pos = add(pos, dirs[current_dir_idx])

        if next_pos in region:
            history.append(next_pos)
            dir_history.append(dirs[current_dir_idx])
            pos = next_pos 
        else:
            current_dir_idx = (current_dir_idx + 1) % 4
            history.append(pos)
            dir_history.append(dirs[current_dir_idx])

        for idx in range(len(history) - 1): 
            if history[idx] == pos and dir_history[idx] == dirs[current_dir_idx]:
                complete_cycle = True
                cycle_start_idx = idx
                break

    return len(history[cycle_start_idx:]) - 1

pmap = Map(sys.argv[1])
pmap.show_map()
regions = find_regions(pmap)
total_area = 0
for region in regions:
    print(f"{pmap[region[0]]}: {region} ({len(region)}")
    total_area += len(region)

print(total_area)

total_cost = 0
for region in regions:
    perimeter = traverse(region)
    print(f"Total cost for region {pmap[region[0]]} is permieter {perimeter} x area {len(region)} = {perimeter * len(region)}")
    total_cost += perimeter * len(region)

print(total_cost)

