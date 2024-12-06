rules, pages = [], []

class Page:
    ordering_rules = {}

    def __init__(self, page_num):
        self.page_num = page_num

    def __lt__(self, other_page):
        return self.page_num in self.ordering_rules.get(other_page.page_num, [])

    def __eq__(self, other_page):
        return self.page_num == other_page.page_num

    def __le__(self, other_page):
        return self.__lt__(other_page) or self.__eq__(other_page)

    def __repr__(self):
        return f"{self.page_num}"

with open('../input.txt') as f:
    for line in f:
        if '|' in line:
            rules.append(line.replace('\n', ''))
        elif ',' in line:
            pages.append(line.replace('\n', ''))

rules_dict: dict[int, list[int]] = {}

for rule in rules:
    gte, lte = [int(x) for x in rule.split('|')]

    if rules_dict.get(gte, False):
        rules_dict[gte].append(lte)
    else:
        rules_dict[gte] = [lte]

# Define Class Attribute
Page.ordering_rules = rules_dict

orderings = [[Page(int(x)) for x in page.split(',')] for page in pages]

middle_sum = 0
middle_sum_incorrect = 0

for ordering in orderings:
    print(ordering)
    if all([ordering[i + 1] <= ordering[i] for i in range(len(ordering) - 1)]):
        print(ordering)
        middle_sum += ordering[(len(ordering) - 1) // 2].page_num
    else:
        middle_sum_incorrect += sorted(ordering)[(len(ordering) - 1) // 2].page_num


print('Part A:')
print(middle_sum)

print('Part B:')
print(middle_sum_incorrect)
