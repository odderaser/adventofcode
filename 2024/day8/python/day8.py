import sys
from itertools import combinations

def parse_input(filename):
    antenna_map = []
    with open(filename) as f:
        for line in f:
            line = line.replace('\n', '')
            if len(line) > 0:
                antenna_map.append([c for c in line]) 
    
    return antenna_map, (len(antenna_map), len(antenna_map[0]))

def determine_antenna_locations(antenna_map):
    antennas = {}
    for row_idx in range(len(antenna_map)):
        for col_idx in range(len(antenna_map[0])):
            char = antenna_map[row_idx][col_idx]
            if char != '.':
                if antennas.get(char, None) is None:
                    antennas[char] = [(row_idx, col_idx)]
                else:
                    antennas[char].append((row_idx, col_idx))

    return antennas

def show_map(amap, antinodes_list=None):
    for r_idx in range(len(amap)):
        for c_idx in range(len(amap[0])):
            char = amap[r_idx][c_idx]
            if antinodes_list is not None and (r_idx, c_idx) in antinodes_list and char == '.':
                print("#", end="")
            else:
                print(char, end="")
        print("")

def inv(vec):
    return (vec[0] * -1, vec[1] * -1)

def diff(pos1, pos2):
    return (pos2[0] - pos1[0], pos2[1] - pos1[1])

def add(pos, vec):
    return (pos[0] + vec[0], pos[1] + vec[1])

def mult(vec, k):
    return (k * vec[0], k * vec[1])

def flatten(xss):
    return [x for xs in xss for x in xs]

def oob(pos):
    if pos[0] < 0 or pos[0] >= map_size[0]:
        return True 
    elif pos[1] < 0 or pos[1] >= map_size[1]:
        return True 
    return False 

def compute_antinodes(antenna_dict):
    antinode_locations = {}
    for key in antenna_dict.keys():
        for ac in combinations(antenna_dict[key], 2): 
            adiff = diff(ac[0], ac[1])
            if key not in antinode_locations.keys():
                antinode_locations[key] = []
            antinode_locations[key].append(add(ac[1], adiff)) 
            k = 2
            while not oob(add(ac[1], mult(adiff, k))):
                print(add(ac[1], mult(adiff, k)))
                antinode_locations[key].append(add(ac[1], mult(adiff, k))) 
                k += 1
                                               
            antinode_locations[key].append(add(ac[0], inv(adiff)))
            k = 2
            while not oob(add(ac[0], mult(inv(adiff), k))):
                antinode_locations[key].append(add(ac[0], mult(inv(adiff), k)))
                k += 1

    return antinode_locations

amap, map_size = parse_input(sys.argv[1])
print(f"Map size: {map_size}")
antenna_locs = determine_antenna_locations(amap)
#show_map(amap)
antinodes = compute_antinodes(antenna_locs)
show_map(amap, antinodes_list=flatten(list(antinodes.values())))
amap, map_size = parse_input(sys.argv[1])
antinode_locs = flatten(list(antinodes.values()))

print(f"Total num of antinode locations = {len(antinode_locs)}")

rm_an = []
for idx in range(len(antinode_locs)):
    an = antinode_locs[idx]
    if an[0] < 0 or an[0] >= map_size[0]:
        rm_an.append(idx)
    elif an[1] < 0 or an[1] >= map_size[1]:
        rm_an.append(idx)

for index in sorted(rm_an, reverse=True):
    del antinode_locs[index]


print(f"Total num in bound antinode locations = {len(antinode_locs)}")
print(f"Num unique antinode locations = {len(set(antinode_locs + flatten(list(antenna_locs.values()))))}")


