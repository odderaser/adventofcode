lines = []

with open('../input.txt') as f:
    for line in f:
        lines.append(line.replace('\n', ''))


print(f"Dimensions: {len(lines)} x {len(lines[0])}")

def search_line(haystack, needle):
    result = 0
    for idx in range(len(haystack) - len(needle) + 1):
        if haystack[idx:(idx + len(needle))] == needle:
            result += 1

    return result

def rotate_lines(lines):

    result = []

    for idx in range(len(lines)):
        _result = ''
        for idy in range(len(lines)):
            _result += lines[idy][idx]
        result.append(_result)

    return result

def diagnalize_lines(lines):

    result = []

    for n in range(2 * len(lines)):
        _result = ""
        for i in range(len(lines)):
            for j in range(len(lines)):
                if (i + j) == n:
                    _result += lines[j][i]
        result.append(_result)

    return result

result = 0

for line in lines:
    result += search_line(line, 'XMAS')
    result += search_line(line[::-1], 'XMAS')

for line in rotate_lines(lines):
    result += search_line(line, 'XMAS')
    result += search_line(line[::-1], 'XMAS')

for line in diagnalize_lines(lines):
    result += search_line(line, 'XMAS')
    result += search_line(line[::-1], 'XMAS')

for line in diagnalize_lines(lines[::-1]):
    result += search_line(line, 'XMAS')
    result += search_line(line[::-1], 'XMAS')

print(result)

def grab_square(haystack, x, y, spacer = "", delimiter=""):

    result = ""
    for row in range(3):
        if row % 2 == 0:
            _result = haystack[y + row][x] + spacer + haystack[y + row][x + 2] 
        else:
            _result = spacer + haystack[y + row][x + 1] + spacer 
        result += _result + delimiter

    return result

solutions = ['MSAMS', 'MMASS', 'SMASM', 'SSAMM']

result = 0

for x in range(len(lines) - 2):
    for y in range(len(lines) - 2):
        if grab_square(lines, x, y) in solutions:
            #print(grab_square(lines, x, y, spacer = ".", delimiter='\n'))
            result += 1

print(result)



