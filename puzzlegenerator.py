import random

import numpy as np

gridLen = 12
final_array = np.full([gridLen, gridLen], '-')

words = ["KARNATAKA", "DELHI", "Kerala", "Manipur", "Mizoram", "Tripura", "Assam", "Sikkim", "Uttarakhand"]


def fillBlanks():
    print(final_array)


def fillWordGrid():
    tempData = generateGridPositions()

    for word in tempData.keys():
        orientation = tempData[word][0]
        row = tempData[word][1]
        col = tempData[word][2]

        # print('row:', row, ' col:', col, 'orientation', orientation, 'word:', word)

        overlapping = checkIfOverlapping(final_array, word, row, col, orientation);
        print("isOverlapping:", overlapping, 'word:', word)
        if overlapping:
            row, col, tempData = generateNonOverlappingIndex(tempData, word, row, col, orientation);

        ## TODO : Overlapping cell values
        ## TODO : Configurable Repeatability

        for c in word:
            # if final_array[row - 1][col - 1] != '-':
            #     print('OVERWRITE ALARM!! row', row - 1, "col:", col - 1)

            final_array[row - 1][col - 1] = c
            if orientation == 'Sleeping':
                col = col + 1
            elif orientation == 'Standing':
                row = row + 1
            else:
                row = row + 1
                col = col + 1
    ## TODO : Implement Diag Left Orientation
    ## TODO : Fill unfiiled cells with random charaters
    # print(final_array)


def generateUniqueIndex():
    randomValues = list(range(1, 12))
    random.shuffle(randomValues)

    return randomValues


def generateGridPositions():
    longestStr = max(words, key=len)
    if (len(longestStr)) > gridLen:
        print("Error")
    wordCount = len(words)
    tempData = dict()
    # orientations = ['Sleeping', 'Standing', 'Diag-Right', 'Diag-Left']
    orientations = ['Sleeping', 'Standing']

    rowIndexList = generateUniqueIndex()
    colIndexList = generateUniqueIndex()

    print("rowIndexList:", rowIndexList)

    for word in words:
        word = get_if_reversed(word)
        wordLen = len(word)

        orientation = random.choice(orientations)
        if orientation == 'Sleeping':
            row = rowIndexList.pop(0)
            col = random.randint(1, (gridLen - wordLen))

        elif orientation == 'Standing':
            row = random.randint(1, (gridLen - wordLen))
            col = colIndexList.pop(0)
        else:
            row = rowIndexList.pop(0)
            col = colIndexList.pop(0)

        tempData[word] = [orientation, row, col]

    print(tempData)
    return tempData


def checkIfOverlapping(tempData, word, row, col, orientation):
    overlapping = False
    for c in word:
        if (tempData[row][col]) != '-':
            overlapping = True;
            break
        if orientation == 'Sleeping':
            col = col + 1
        elif orientation == 'Standing':
            row = row + 1
        else:
            row = row + 1
            col = col + 1
    return overlapping


def generateNonOverlappingIndex(tempData, word, row, col, orientation):
    return row, col


# def fixOverLappingIndex(tempData):
#     orientationData = dict()
#
#     for word in tempData.keys():
#         orientation = tempData[word][0]
#         if orientation in orientationData.keys() :
#             orientationData[orientation].append(word)
#         else:
#             orientationData[orientation] = [word]
#
#     print(orientationData)
#     return tempData

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
