import sys
from math import floor, log10
from functools import lru_cache

def parse_input(filename):
    with open(filename) as f:
        for line in f:
            return line.replace('\n', '').split(' ')

def oneblink(stones):
    new_stone_list = []
    for x in stones:
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

@lru_cache(maxsize=None)
def _blink(x):
    if x == '0':
        return ['1']
    else:
        lenx = floor(log10(int(x))) + 1
        if lenx % 2 == 0:
            return [x[0:(lenx // 2)], str(int(x[(lenx // 2):lenx]))]
        else:
            return [str(int(x) * 2024)]

@lru_cache(maxsize=None)
def _twoblink(x):
    print(f"x = {x}")
    if x == '0':
        #print("returning 2024 since 0 -> 1 -> 2024")
        print("Returning ['2024']")
        return ['2024']
    else:
        lenx = floor(log10(int(x))) + 1
        if lenx % 4 == 0:
            #print("Splitting into 4s since lenx % 4 == 0")
            chunk_size = (lenx + 4 - 1) // 4 
            print(f"Returning {[x[i:i + chunk_size] for i in range(0, lenx, chunk_size)]}")
            return [x[i:i + chunk_size] for i in range(0, lenx, chunk_size)] 
        elif lenx % 2 == 0:
            #print("Splitting into 2 and multiplying by 2024")
            first_split = str(int(x[0:(lenx // 2)]) * 2024) 
            second_split = int(x[(lenx // 2):lenx]) 
            if second_split == 0:
                second_split == 1
            else:
                second_split = second_split * 2024
            print("DUDE")
            print(f"Returning {[first_split, str(second_split)]}")
            return [first_split, str(second_split)] 
        else:
            #print("multiplying by 2024 and splitting by 2")
            val = int(x) * 2024
            lenx = floor(log10(val)) + 1
            if lenx % 2 == 0:
                print('amihere?')
                print(f"Returning {[str(val)[0:(lenx // 2)], str(int(str(val)[(lenx // 2):lenx]))]}")
                return [str(val)[0:(lenx // 2)], str(int(str(val)[(lenx // 2):lenx]))]
            else:
                print(f"THIS IS A NONO Returning {[str(int(x) * 2024)]}")
                return [str(int(x) * 2024)]



def blink(stones):
    new_stone_list = []
    for x in stones:
        new_stone_list.extend(_twoblink(x))

    return new_stone_list


stones = parse_input(sys.argv[1])
#print(stones)
N = int(sys.argv[2])

for nblinks in range(1, N + 1, 1):
    stones = oneblink(stones)
    print(f"After {nblinks} blinks: {stones}")
    print(f"After {nblinks} blinks, there are {len(stones)} stones.")


