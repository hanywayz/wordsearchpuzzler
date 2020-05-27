import random
import string

import numpy as np
import pandas as pd
import pdfkit

gridLen = 12
# TODO : Read from configuration file
words = ["Karnataka", "Delhi", "Kerala", "Manipur", "Mizoram", "Tripura", "Assam", "Sikkim", "Uttarakhand"]

# TODO : Read headers
# TODO : Paging Logic
# TODO : Page Size A5

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
            if count > 30:
                print("Gridlock Detected!! Retrying!")
                fillWordGrid()
                return

        filledInWords.append([word, orientation, row, col])

    print(filledInWords)

    final_array = generateFinalGrid(filledInWords)
    print(final_array)
    generate_html(words, final_array, 1)

    final_array_withgibberish = fillInGibberish(final_array)
    print(final_array_withgibberish)
    generate_html(words, final_array_withgibberish, 2)


def generate_html(words, final_array, val):
    # TODO : Use a templating engine

    df = pd.DataFrame(final_array)
    html = df.to_html(index=False, header=False)
    print(html)

    reshaped_words = np.reshape(words, (-1, 3))
    words_df = pd.DataFrame(reshaped_words)
    words_html = words_df.to_html(index=False, header=False)
    print(words_html)

    base_html = '<!DOCTYPE html><html><head><style> table{border-spacing: 0;border-collapse: collapse;margin-left:auto; margin-right:auto;}td{ border-bottom: 1px solid black !important; text-align: center; vertical-align: middle; font-size : 24px; padding:10px; height: 3vw; width: 3vw;}th{	border-bottom: 1px solid black !important;  text-align: center;}.pageheader{	text-align: center; 	font-size : 30px;font-weight: bold;}</style></head><body><p class=\'pageheader\'> TITLE_TO_REPLACE</p> TABLE_TO_REPLACE<p><br><hr/><br>WORDS_TO_REPLACE</p></body></html>'
    html = base_html.replace("TABLE_TO_REPLACE", html)
    html = html.replace("TITLE_TO_REPLACE", 'Name of Indian States')
    html = html.replace("WORDS_TO_REPLACE", words_html)

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    output_file = "C://Users/sourav/Desktop/samples/out" + str(val) + ".pdf"

    options = {'page-size': 'A5', 'dpi': 400}

    pdfkit.from_string(html, output_file, configuration=config,options=options)


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
            if final_array[x, y] == '-':
                final_array[x, y] = random.choice(string.ascii_uppercase)

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
