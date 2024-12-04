import re

text = None
with open('../input.txt') as input_file:
    text = input_file.read()

mul_regex = re.compile(r"mul\((\d+),(\d+)\)")

product = 0
start_pos = 0

while True:
   match = mul_regex.search(text, start_pos)
   print(match)
   if match:
       start_pos = match.span()[1]
       product += (int(match.groups()[0]) * int(match.groups()[1])) 
   else:
        break

print(f"Total sum: {product}")

