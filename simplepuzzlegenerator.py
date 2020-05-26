import random
import string

import numpy as np

gridLen = 12

words = ["KARNATAKA", "DELHI", "Kerala", "Manipur", "Mizoram", "Tripura", "Assam", "Sikkim", "Uttarakhand"]


def fillWordGrid():
    filledInWords = list()

    for word in words:
        word = word.upper()
        word = get_if_reversed(word)
        wordLen = len(word)

        orientations = ['HORIZONTAL', 'VERTICAL', 'DIAGFORWARD', 'DIAGBACKWARD']
        # orientations = ['HORIZONTAL', 'VERTICAL', 'DIAGFORWARD']
        orientation = random.choice(orientations)

        count = 0
        isOverlapping = True
        while isOverlapping:
            col, row = getStartPostion(orientation, wordLen)
            isOverlapping = checkIfOverlapping(word, row, col, orientation, filledInWords)
            count = count + 1
            if count > 100:
                print("Gridlock")
                return

        filledInWords.append([word, orientation, row, col])

    print(filledInWords)

    final_array = generateFinalGrid(filledInWords)
    print(final_array)
    final_array = fillInGibberish(final_array)
    print(final_array)


def generateFinalGrid(filledInWords):
    final_array = np.full([gridLen, gridLen], '-')
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
            elif orientation == 'DIAGFORWARD':
                row = row + 1
                col = col + 1
            elif orientation == 'DIAGBACKWARD':
                row = row + 1
                col = col - 1

    return final_array


def fillInGibberish(final_array):
    for x in range(0, final_array.shape[0]):
        for y in range(0, final_array.shape[1]):
            if final_array[x, y] == '-' :
                final_array[x, y] = random.choice(string.ascii_uppercase)
    print(final_array)
    return final_array


def getStartPostion(orientation, wordLen):
    if orientation == 'HORIZONTAL':
        row = random.randint(0, 11)
        col = random.randint(0, (gridLen - wordLen - 1))
    elif orientation == 'VERTICAL':
        row = random.randint(0, (gridLen - wordLen - 1))
        col = random.randint(0, 11)
    elif orientation == 'DIAGFORWARD':
        row = random.randint(0, (gridLen - wordLen - 1))
        col = random.randint(0, (gridLen - wordLen - 1))
    elif orientation == 'DIAGBACKWARD':
        row = random.randint(0, (gridLen - wordLen - 1))
        col = random.randint(wordLen, gridLen - 1)

    return col, row


def checkIfOverlapping(word, row, col, orientation, filledInWords):
    wordCells = getCells(word, row, col, orientation)

    # print("CHECK OVERLAP word:", word)

    for filledInWord in filledInWords:
        tempWordCells = getCells(filledInWord[0], filledInWord[2], filledInWord[3], filledInWord[1])
        for refCell in tempWordCells:
            for wordCell in wordCells:
                if refCell[1] == wordCell[1] and refCell[2] == wordCell[2]:
                    return True
        # print("CheckIfOverlapping word:", word, "filledInWord[0]:",filledInWord[0], "overlapping:",overlapping)
    return False


def getCells(word, row, col, orientation):
    cells = list()
    for c in word:
        cells.append([c, row, col])
        if orientation == 'HORIZONTAL':
            col = col + 1
        elif orientation == 'VERTICAL':
            row = row + 1
        elif orientation == 'DIAGFORWARD':
            row = row + 1
            col = col + 1
        elif orientation == 'DIAGBACKWARD':
            row = row + 1
            col = col - 1
    return cells


def get_if_reversed(word):
    is_reverse = random.randint(0, 1)
    if is_reverse:
        word = word[::-1]
    return word


class WordSearchGenerator:
    if __name__ == "__main__":
        fillWordGrid()
