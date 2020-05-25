import random

import numpy as np

gridLen = 12
final_array = np.full([gridLen, gridLen], '-')

words = ["KARNATAKA", "DELHI", "Kerala", "Manipur", "Mizoram", "Tripura", "Assam", "Sikkim", "Uttarakhand"]


def fillWordGrid():
    rowIndexList = generateUniqueIndex()
    colIndexList = generateUniqueIndex()

    filledInWords = list()

    for word in words:
        word = get_if_reversed(word)
        wordLen = len(word)

        # orientations = ['HORIZONTAL', 'VERTICAL', 'DIAGONAL']
        orientations = ['HORIZONTAL', 'VERTICAL']

        orientation = random.choice(orientations)
        if orientation == 'HORIZONTAL':
            row = rowIndexList.pop(0)
            col = random.randint(0, (gridLen - wordLen - 1))
        elif orientation == 'VERTICAL':
            row = random.randint(0, (gridLen - wordLen - 1))
            col = colIndexList.pop(0)
        else:
            # TODO : Fix based on max length
            row = rowIndexList.pop(0)
            col = colIndexList.pop(0)

        print("word:", word, "row:", row, "col:", col, "orientation:", orientation)

        isOverlapping = checkIfOverlapping(final_array, word, row, col, orientation)

        print("isOverlapping", isOverlapping, "word:", word)

        if isOverlapping:
            # if orientation == 'HORIZONTAL':
            #     col =
            # elif orientation == 'VERTICAL':
            #     row =
            # else:
            #
            conflictingWords = filledInWords

            row, col = resolveConflicts(word, row, col, orientation,conflictingWords)
        
        for c in word:
            final_array[row][col] = c
            if orientation == 'HORIZONTAL':
                col = col + 1
            elif orientation == 'VERTICAL':
                row = row + 1
            else:
                row = row + 1
                col = col + 1

        filledInWords.append(word)

    print(final_array)


def resolveConflicts(word, row, col, orientation, conflictingWords):
    return row, col


def generateUniqueIndex():
    randomValues = list(range(0, 11))
    random.shuffle(randomValues)
    return randomValues


def checkIfOverlapping(tempData, word, row, col, orientation):
    overlapping = False
    for c in word:
        if (tempData[row][col]) != '-':
            overlapping = True;
            break
            
        if orientation == 'HORIZONTAL':
            col = col + 1
        elif orientation == 'VERTICAL':
            row = row + 1
        else:
            row = row + 1
            col = col + 1
    return overlapping

def get_if_reversed(word):
    word = word.upper()
    is_reverse = random.randint(0, 1)
    if is_reverse:
        word = word[::-1]
    return word

class WordSearchGenretor:
    if __name__ == "__main__":
        fillWordGrid()
