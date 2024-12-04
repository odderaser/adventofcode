import re

text = None
with open('../input.txt') as input_file:
    text = input_file.read()

mul_regex = re.compile(r"mul\((\d+),(\d+)\)")
dont_regex = re.compile(r"([\s\S]*?)don't\(\)")
do_dont_regex = re.compile(r"do\(\)([\w\W\s\S]*?)(don't\(\)|$)")

product = 0
start_pos = 0
end_pos = 0

batch = dont_regex.search(text, start_pos)
while batch:  
    print(batch)
    start_pos, end_pos = batch.span(1)
    match = mul_regex.search(text, start_pos, end_pos) 
    while match:
        start_pos = match.span()[1]
        product += (int(match.groups()[0]) * int(match.groups()[1]))
        match = mul_regex.search(text, start_pos, end_pos)
    batch = do_dont_regex.search(text, start_pos)

print(f"Total sum: {product}")
