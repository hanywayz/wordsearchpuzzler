import random

import numpy as np

gridLen = 12
final_array = np.full([gridLen, gridLen], '-')

words = ["KARNATAKA", "DELHI", "Kerala", "Manipur", "Mizoram", "Tripura", "Assam","Sikkim","Uttarakhand"]


def fillBlanks():
    print(final_array)


def fillWordGrid():
    tempData = generateGridPositions()

    for word in tempData.keys():
        orientation = tempData[word][0]
        row = tempData[word][1]
        col = tempData[word][2]

        print('row:', row, ' col:', col, 'orientation', orientation, 'word:', word)

        ## TODO : Overlapping row and columns
        ## TODO : Overlapping cell values

        for c in word:
            final_array[row - 1][col - 1] = c
            if orientation == 'Sleeping':
                col = col + 1
            elif orientation == 'Standing':
                row = row + 1
            else:
                row = row + 1
                col = col + 1

    ## TODO : Fill unfiiled cells with random charaters
    # print(final_array)


def generateUniqueIndex():
    list = []
    for i in range(5):
        r = random.randint(1, gridLen)
        if r not in list: list.append(r)
    return list


def generateGridPositions():
    longestStr = max(words, key=len)
    if (len(longestStr)) > gridLen:
        print("Error")
    wordCount = len(words)
    tempData = dict()
    orientations = ['Sleeping', 'Standing', 'Diag-Right', 'Diag-Left']
    # orientations = ['Sleeping']

    rowIndexList = generateUniqueIndex()
    colIndexList = generateUniqueIndex()

    for word in words:
        word = get_if_reversed(word)
        wordLen = len(word)

        orientation = random.choices(orientations)
        if orientation == 'Sleeping':
            row = rowIndexList[0]
            rowIndexList.remove(0)
            col = random.randint(1, (gridLen - wordLen))
        elif orientation == 'Standing':
            row = random.randint(1, (gridLen - wordLen))
            col = colIndexList[0]
            colIndexList.remove(0)
        else:
            row = random.randint(1, (gridLen - wordLen))
            col = random.randint(1, (gridLen - wordLen))

        tempData[word] = [orientation[0], row, col]
    print(tempData)
    return tempData


def get_if_reversed(word):
    word = word.upper()
    is_reverse = random.randint(0, 1)
    if is_reverse:
        word = word[::-1]
    return word


class WordSearchGenretor:
    if __name__ == "__main__":
        fillWordGrid()
        fillBlanks()
