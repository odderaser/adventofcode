from math import copysign

reports = []

with open('../input.txt') as input_file:
    for line in input_file:
        line = line.replace('\n', '')
        if line != '':
            reports.append([int(x) for x in line.split(' ')])

def check_report_safety(report, dampener_active=False):

    level_diffs = [y - x for x, y in zip(report[:-1], report[1:])]

    level_abs = [abs(d) <= 3 and abs(d) != 0 for d in level_diffs]
    level_sign = [copysign(1, d) for d in level_diffs] 
    primary_sign = max(set(level_sign), key=level_sign.count)
    level_sign = [s == primary_sign for s in level_sign]

    level_mask = [a and s for a, s in zip(level_abs, level_sign)]

    if all(level_mask):
        return True
    elif dampener_active: 
        return any([check_report_safety(report[:(idx)] + report[(idx + 1):]) for idx in range(len(report))]) 
    else:
        return False


safe_reports = 0
safe_dampened_reports = 0

tests = [
            [7, 6, 4, 2, 1],
            [1, 2, 7, 8, 9],
            [9, 7, 6, 2, 1],
            [1, 3, 2, 4, 5],
            [8, 6, 4, 4, 1],
            [1, 3, 6, 7, 9]
    ]

expected = [True, False, False, False, False, True]
expected_dampened = [True, False, False, True, True, True]

print('==== Tests w/o dampener ====')
for test, expected in zip(tests, expected):
    print(f"{test} : {check_report_safety(test)}, expected: {expected}") 

print('==== Tests w/ dampener ====')
for test, expected in zip(tests, expected_dampened):
    print(f"{test} : {check_report_safety(test, dampener_active=True)}, expected: {expected}") 

for report in reports:
    if check_report_safety(report):
        safe_reports += 1

    if check_report_safety(report, dampener_active=True):
        safe_dampened_reports += 1

print(f"Number of safe reports: {safe_reports}")
print(f"Number of safe reports w/ dampener: {safe_dampened_reports}")


