import sys
import itertools

def parse_input(filename):
    with open(filename) as f:
        for line in f:
            return list(line.replace('\n', ''))

def get_block_map(disk_map):
    result = []
    for i, x in enumerate(itertools.batched(disk_map, 2)):
        f = int(x[0])
        if len(x) == 2:
            fs = int(x[1])
        else:
            fs = 0 
        result += [str(i)] * f + ["."] * fs

    return list(result)

def fs_loc(block_map):
    fs_locs = []
    for idx in range(len(block_map)-1, -1, -1):
        if block_map[idx] == '.':
            fs_locs.append(idx)

    return fs_locs

def grouped_fs_loc(block_map):
    fs_locs = {}
    idx = 0
    starting_idx = -1
    while idx < len(block_map):
        if block_map[idx] != '.':
            starting_idx = -1
        elif starting_idx != -1:
            fs_locs[starting_idx] += 1
        elif block_map[idx] == '.':
            starting_idx = idx
            fs_locs[starting_idx] = 1
        idx += 1

    return fs_locs 

def grouped_files(block_map):
    f_locs = {}
    idx = 0
    current_file_id = None
    while idx < len(block_map):
        # Free space, do nothing
        if block_map[idx] == '.':
            pass
        # Add to existing file
        elif block_map[idx] == current_file_id:
            f_locs[current_file_id]['length'] += 1
        # Found new? non free space
        elif block_map[idx] != '.':
            current_file_id = block_map[idx]
            if f_locs.get(current_file_id, None) is None:
                f_locs[current_file_id] = {}
            f_locs[current_file_id]['starting_idx'] = idx
            f_locs[current_file_id]['length'] = 1
        idx += 1

    return f_locs

def get_next_fs(block_map):
    idx = 0
    while block_map[idx] != '.' and idx < len(block_map):
        idx += 1

    if idx >= len(block_map):
        raise ValueError

    return idx

def get_last_f(block_map):
    idx = len(block_map) - 1
    while block_map[idx] == '.' and idx >= 0:
        idx -= 1
    return idx

def compress_filespace(disk_map, show=False):
    block_map = get_block_map(disk_map)
    fs_locs = fs_loc(block_map)
    num_free = sum([x == "." for x in block_map]) 
    while not all([x == "." for x in block_map[-num_free:-1]]):
        fs_idx, f_idx = fs_locs.pop(), get_last_f(block_map)
        block_map[fs_idx], block_map[f_idx] = block_map[f_idx], block_map[fs_idx]
        if show:
            print("".join(block_map))

    return block_map

def group_compress_filespace(disk_map, show=False):
    block_map = get_block_map(disk_map)
    gfs_locs = grouped_fs_loc(block_map)
    gf_locs = grouped_files(block_map)
    for file_id in reversed(list(gf_locs.keys())): 
        print(f"Checking {file_id}")
        file_length = gf_locs[file_id]['length']
        f_sidx, f_length = gf_locs[file_id]['starting_idx'], gf_locs[file_id]['length']
        for fs_sidx, fs_length in gfs_locs.items():
            if file_length <= fs_length and fs_sidx < f_sidx:
                block_map[fs_sidx:(fs_sidx + f_length)], block_map[f_sidx:(f_sidx + f_length)] = block_map[f_sidx:(f_sidx + f_length)], block_map[fs_sidx:(fs_sidx + f_length)]  
                remaining_fs_length = fs_length - f_length
                print(f"modifying gfs_locs[{fs_sidx}] = {gfs_locs[fs_sidx]}")
                del gfs_locs[fs_sidx]
                if remaining_fs_length > 0:
                    gfs_locs[fs_sidx + f_length] = remaining_fs_length
                    print(f"... to gfs_locs[{fs_sidx + f_length}] = {remaining_fs_length}")
                # Check if freed fs space falls within existing fs blocks 

                if show:
                    print(''.join(block_map))
                break

    print(gfs_locs)

    return block_map

def checksum(block_map):
    result = 0
    for i, f in enumerate(block_map):
        if f != '.':
            result += i * int(f)
    return result

disk_map = parse_input(sys.argv[1])
print(''.join(get_block_map(disk_map)))
grouped_compressed_block_map = group_compress_filespace(disk_map, show=True)
print(checksum(grouped_compressed_block_map))

