import sys

def parse_input(filename):
    tmap = []
    with open(filename) as f:
        for line in f:
            tmap.append([int(x) for x in line.replace('\n', '')])

    return tmap, (len(tmap), len(tmap[0]))

def show_map(tmap):
    for row in tmap:
        for col in row:
            print(col, end="")
        print("")

def get_trailheads(tmap):
    trailheads = []
    for ridx in range(len(tmap)):
        for cidx in range(len(tmap[0])):
            if tmap[ridx][cidx] == 0:
                trailheads.append((ridx, cidx))

    return trailheads

def oob(pos):
    if pos[0] < 0 or pos[0] >= map_size[0]:
        return True
    elif pos[1] < 0 or pos[1] >= map_size[1]:
        return True
    return False 

def add(pos, vec):
    return (pos[0] + vec[0], pos[1] + vec[1])

def available_dirs(pos, tmap):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    result = []
    pos_val = tmap[pos[0]][pos[1]]
    for adir in dirs:
        ppos = add(pos, adir)
        if not oob(ppos) and (tmap[ppos[0]][ppos[1]] - pos_val) == 1:
            result.append(ppos)

    return result

def dfs(trailhead, tmap):
    score = 0
    stack = available_dirs(trailhead, tmap)

    while len(stack) > 0:
        pos = stack.pop()
        pos_value = tmap[pos[0]][pos[1]]
        if pos_value == 9:
            score += 1
        for adir in available_dirs(pos, tmap):
            stack.append(adir)

    print(f"Total trailhead score: {score}")
    return score

tmap, map_size = parse_input(sys.argv[1])
show_map(tmap)
trailheads = get_trailheads(tmap)
score = 0
for th in trailheads:
    score += dfs(th, tmap)

print(f"Total Trailhead Score: {score}")
