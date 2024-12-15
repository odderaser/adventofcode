import sys
from itertools import product 

def parse_input(filename):
    soln_list, values_list = [], []
    with open(filename) as f:
        for line in f:
            split_line = line.split(':')
            values_list.append([int(x) for x in split_line[1].replace('\n', '').split(' ') if x != '']) 
            soln_list.append(int(split_line[0]))

    return soln_list, values_list 

soln_list, values_list = parse_input(sys.argv[1])

def minimath(value1, value2, op):
    if op == '+':
        return value1 + value2
    elif op == '*':
        return value1 * value2
    elif op == "||":
        return int(str(value1) + str(value2))
    else:
        raise ValueError

def evaluate_expression(values, operators):

    result = minimath(values[0], values[1], operators[0])

    for idx in range(2, len(values)):
        result = minimath(result, values[idx], operators[idx - 1])

    return result

result = 0

for soln, values in zip(soln_list, values_list):
    for op_array in product(["*", "+", "||"], repeat=len(values) - 1):
        if evaluate_expression(values, op_array) == soln:
            result += soln 
            break

print(f"Total sum is {result}")
