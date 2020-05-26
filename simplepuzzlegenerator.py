import random

import numpy as np

gridLen = 12
final_array = np.full([gridLen, gridLen], '-')

words = ["KARNATAKA", "DELHI", "Kerala", "Manipur", "Mizoram", "Tripura", "Assam", "Sikkim", "Uttarakhand"]


def fillWordGrid():
    filledInWords = list()

    for word in words:
        word = word.upper()
        word = get_if_reversed(word)
        wordLen = len(word)

        orientations = ['HORIZONTAL', 'VERTICAL']

        orientation = random.choice(orientations)
        col, row = getRowCol(orientation, wordLen)
        isOverlapping = True
        while isOverlapping:
            isOverlapping = checkIfOverlapping(word, row, col, orientation, filledInWords)
            if isOverlapping:
                col, row = getRowCol(orientation, wordLen)

        filledInWords.append([word, orientation, row, col])

        # print("word:", word, "row:", row, "col:", col, "orientation:", orientation)

    print(filledInWords)

    for eachWord in filledInWords:
        row = eachWord[2]
        col = eachWord[3]
        orientation = eachWord[1]
        for c in eachWord[0]:
            final_array[row][col] = c
            if orientation == 'HORIZONTAL':
                col = col + 1
            elif orientation == 'VERTICAL':
                row = row + 1
    print(final_array)


def getRowCol(orientation, wordLen):
    if orientation == 'HORIZONTAL':
        row = random.randint(0, 11)
        col = random.randint(0, (gridLen - wordLen - 1))
    elif orientation == 'VERTICAL':
        row = random.randint(0, (gridLen - wordLen - 1))
        col = random.randint(0, 11)
    return col, row


def checkIfOverlapping(word, row, col, orientation, filledInWords):
    overlapping = False
    wordCells = getCells(word, row, col, orientation)

    # print("CHECK OVERLAP word:", word)

    for filledInWord in filledInWords:
        tempWordCells = getCells(filledInWord[0], filledInWord[2], filledInWord[3], filledInWord[1])
        for refCell in tempWordCells:
            for wordCell in wordCells:
                if refCell[1] == wordCell[1] and refCell[2] == wordCell[2]:
                    overlapping = True
                    # print("overlapping!!! cell :", wordCell[1], wordCell[2], "word :", word, "row:", row, "col:", col,
                    #       "orientation:", orientation,
                    #       "filledInWord", filledInWord)
                    # print("wordCells", wordCells, "tempWordCells", tempWordCells)
                    return True
        # print("CheckIfOverlapping word:", word, "filledInWord[0]:",filledInWord[0], "overlapping:",overlapping)
    return overlapping


def getCells(word, row, col, orientation):
    cells = list()
    for c in word:
        cells.append([c, row, col])
        if orientation == 'HORIZONTAL':
            col = col + 1
        elif orientation == 'VERTICAL':
            row = row + 1
    return cells


def resolveConflicts(word, row, col, orientation, conflictingWords):
    return row, col


def get_if_reversed(word):
    is_reverse = random.randint(0, 1)
    if is_reverse:
        word = word[::-1]
    return word


class WordSearchGenretor:
    if __name__ == "__main__":
        fillWordGrid()
