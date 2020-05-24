import random
import numpy as np

words = ["Java", "Python", "GoLang", "NodeJs", "DotNet", "Pascal"]

longestStr = max(words, key=len)

if (len(longestStr)) > 12:
    print("Error")

final_array = np.full([12, 12], '-')

for word in words:

    row = random.randint(1, 4)
    col = random.randint(1, 4)

    is_reverse = random.randint(0, 1)

    if is_reverse:
        word = word[::-1]

    direction = random.randint(1, 3)

    for c in word:
        if direction == 1:
            row = row + 1
        elif direction == 2:
            col = col + 1
        else:
            row = row + 1
            col = col + 1
        final_array[row][col] = c

print(final_array)
