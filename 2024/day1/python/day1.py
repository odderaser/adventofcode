from collections import Counter


print('==== Day 1 Part 1 ====')
list1, list2 = [], [] 

with open("../input", "r") as input_file:
    for line in input_file:
        line_split = line.split(' ')
        list1.append(int(line_split[0]))
        list2.append(int(line_split[3].replace('\n', ''))) 

list1.sort(), list2.sort()
total_dist = 0

for idx in range(len(list1)):
    total_dist += abs(list1[idx] - list2[idx])

print(f"Total distance: {total_dist}")

print('==== Day 1 Part 2 ====')

def compute_similarity(list1, list2):
    list2_value_counts = Counter(list2)

    similarity_scores = {}

    for loc_id in list1:
        _similarity_score = loc_id * list2_value_counts.get(loc_id, 0)
        if loc_id in similarity_scores.keys():
            similarity_scores[loc_id] += _similarity_score
        else:
            similarity_scores[loc_id] = _similarity_score

    return similarity_scores

similarity_scores = compute_similarity(list1, list2)

total_similarity_score = 0
for loc_id, similarity_score in similarity_scores.items():
    total_similarity_score += similarity_score

print(f'Total Similarity Score: {total_similarity_score}')

