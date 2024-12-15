import sys
from math import floor, log10
from tqdm import tqdm
from functools import lru_cache 

def parse_input(filename):
    with open(filename) as f:
        for line in f:
            return line.replace('\n', '').split(' ')

def oneblink(stones):
    new_stone_list = []
    for x in stones:
        new_stone_list.extend(_blink(x))

    return new_stone_list

@lru_cache(maxsize=None)
def _blink(x):
    new_stone_list = []
    if x == '0':
        new_stone_list.append('1')
    else:
        lenx = floor(log10(int(x))) + 1
        if lenx % 2 == 0:
            new_stone_list.append(x[0:(lenx // 2)])
            new_stone_list.append(str(int(x[(lenx // 2):lenx]))) 
        else:
            new_stone_list.append(str(int(x) * 2024))

    return new_stone_list




memo = {}

def blink(stones, n, memoize=False, final_pass=False):
    new_stone_list = []
    final_stone_count = 0
    for x in tqdm(stones):
        if memoize and memo.get(x, None) is not None:
            if final_pass:
                final_stone_count += len(memo[x])
            else:
                new_stone_list.extend(memo[x])
        else:
            res = _blinkn([x], n)
            if memoize and len(memo.keys()) < 10000:
                memo[x] = res
            if final_pass:
                final_stone_count += len(res)
            else:
                new_stone_list.extend(res)

    if final_pass:
        return final_stone_count
    else:
        return new_stone_list

def _blinkn(stones, n):
    _stones = oneblink(stones)
    for i in range(1, n):
        _stones = oneblink(_stones)

    return _stones

stones = parse_input(sys.argv[1])
print(stones)

stones = blink(stones, 5, memoize=False)
print(f"After 5 blinks, there are {len(stones)} stones.")
#stones = blink(stones, 6, memoize=True, final_pass=False)
stones = blink(stones, 35, memoize=True, final_pass=False)
print(f"After 40 blinks, there are {len(stones)} stones.")
stones = blink(stones, 35, memoize=True, final_pass=True)
print(f"After 75, there are {stones} stones.")
