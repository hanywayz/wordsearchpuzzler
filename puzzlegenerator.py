import random
import numpy as np

words = ["Java", "Python", "GoLang", "NodeJs", "DotNet", "Pascal"]

longestStr = max(words, key=len)

gridLen = 12

if (len(longestStr)) > gridLen:
    print("Error")

final_array = np.full([gridLen, gridLen], '-')

for word in words:
    word = word.upper()

    wordLen = len(word)

    is_reverse = random.randint(0, 1)

    if is_reverse:
        word = word[::-1]

    direction = random.randint(1, 3)

    if direction == 1:
        row = random.randint(1, (gridLen - wordLen))
        col = random.randint(1, gridLen)
    elif direction == 2:
        row = random.randint(1, gridLen)
        col = random.randint(1, (gridLen - wordLen))
    else:
        row = random.randint(1, (gridLen - wordLen))
        col = random.randint(1, (gridLen - wordLen))

    ## TODO : Overlapping row and columns
    ## TODO : Overlapping cell values
    ## TODO : Fix index logic

    for c in word:
        if direction == 1:
            row = row + 1
        elif direction == 2:
            col = col + 1
        else:
            row = row + 1
            col = col + 1
        final_array[row][col] = c

## TODO : Fill unfiiled cells with random charaters
print(final_array)
