import random
import string

import numpy as np
import pandas as pd
import pdfkit
import yaml
from PyPDF2 import PdfFileMerger


from time import time
import itertools

gridLen = 12

basepath = "C://Users/sourav/Desktop/book_generation/"
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

template_html = '<!DOCTYPE html><html><head><style> body{ background-image: url(\'file:\\\\\\C:\\dev\\book\\bg.png\');background-repeat: no-repeat; background-attachment: fixed; background-size: 100% 100%;border: 1px dashed grey;} table{border-spacing: 0;border-collapse: collapse;margin-left:auto; margin-right:auto;}td{ border-bottom: 1px solid black !important; text-align: center; vertical-align: middle; font-size : 18px; padding:10px; height: 3vw; width: 3vw;}th{	border-bottom: 1px solid black !important;  text-align: center;}.pageheader{	text-align: center; 	font-size : 30px;font-weight: bold;}</style></head><body> <p> <p class=\'pageheader\'> TITLE_TO_REPLACE</p>  <p> TABLE_TO_REPLACE</p><br/><hr style=\'1px dashed grey\'><p>WORDS_TO_REPLACE</p>  <br/></p> <footer style=\'text-align:center\'>Page : PAGE_NO</footer> </body> </html>'


# TODO : Replace '-' with blank space in existing file
# TODO : Puzzle Number
# TODO : Repeatability Logic
# TODO : Fix Page No
# TODO : Apply templates -  cover page, fist page, content etc


def fillWordGrid(words, title):
    filledInWords = list()

    for word in words:
        word = word.upper()
        word = get_if_reversed(word)
        wordLen = len(word)

        orientations = ['HORIZONTAL', 'VERTICAL', 'DIAGFORWARD', 'DIAGBACKWARD']
        orientation = random.choice(orientations)

        count = 0
        isOverlapping = True
        while isOverlapping:
            col, row = getStartPostion(orientation, wordLen)
            isOverlapping = checkIfOverlapping(word, row, col, orientation, filledInWords)
            count = count + 1
            if count > 30:
                print("Gridlock Detected!! Retrying!")
                return fillWordGrid(words, title)

        filledInWords.append([word, orientation, row, col])

    print(filledInWords)

    solution_array = generateFinalGrid(filledInWords)
    problem_array = fillInGibberish(solution_array)

    return problem_array, solution_array


def generate_html(words, input_array, title, page_no):
    html = generatePageHTML(input_array, words, title, page_no)

    return generatePagePDF(html, page_no)


def generatePagePDF(html, page_no):
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    output_file = basepath + "/pages/" + str(page_no) + ".pdf"
    options = {'page-size': 'A5', 'dpi': 400}
    pdfkit.from_string(html, output_file, configuration=config, options=options)
    return output_file

def htmlToPDF(filePath, outputFileName):
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    output_file = basepath + "/pages/" + str(outputFileName) + ".pdf"
    options = {'page-size': 'A5', 'dpi': 400}
    with open(filePath) as f:
        pdfkit.from_file(f, output_file, configuration=config, options=options)
    return output_file


def generate_Content_page(titles, problem_titlepages, solution_titlepages):
    html = '<html> <head> <style> body{background-image: url(\'file:///C:\\Users\\sourav\\Desktop\\book_generation\\footer-background.jpg\');background-repeat: no-repeat; background-attachment: fixed; background-size: 100% 100%;} html{border: dashed;} table{border-spacing: 0;border-collapse: collapse;margin-left:auto; margin-right:auto;}th{font-size : 18px; font-weight:bold}td{ border-bottom: 1px solid black !important; text-align: left; vertical-align: middle; font-size : 16px; padding:10px; }th{	border-bottom: 1px solid black !important;  text-align: center;}.pageheader{text-align: center;font-size : 30px;font-weight: bold;}</style> </head>'
    html = html + '<body ><p style=\'text-align:center;font-weight:bold;font-size : 24px;\'> Problems and Solutions </p> <hr><br>'
    html = html + '<table>'

    for (probs, sols) in zip(problem_titlepages, solution_titlepages):
            html = html + '<tr><td>' + probs[0] + '</td><td>' + str(probs[1]) + '</td><td></td><td>' + str(sols[1]) + '</td></tr>'

    html = html + '</table> </body> </html>'

    return generatePagePDF(html, "content")


def generatePageHTML(input_array, words, title, page_no):
    df = pd.DataFrame(input_array)
    df = df.replace('-', '*')
    puzzle_html = df.to_html(index=False, header=False)

    reshaped_words = np.reshape(words, (-1, 3))
    words_df = pd.DataFrame(reshaped_words)
    words_html = words_df.to_html(index=False, header=False)

    html = template_html.replace("TABLE_TO_REPLACE", puzzle_html)
    html = html.replace("TITLE_TO_REPLACE", title)
    html = html.replace("WORDS_TO_REPLACE", words_html)
    html = html.replace("PAGE_NO", str(page_no))

    return html


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
    new_array = np.array(final_array)
    for x in range(0, new_array.shape[0]):
        for y in range(0, new_array.shape[1]):
            if new_array[x, y] == '-':
                new_array[x, y] = random.choice(string.ascii_uppercase)

    return new_array


def getStartPostion(orientation, wordLen):
    try:
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
    except:
        print(wordLen, orientation)

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


def printBook(problem_puzzle_files, solution_puzzle_files, content_page):
    merger = PdfFileMerger()
    tempPath = basepath + "/pages/"
    merger.append(open(tempPath + "1.pdf", 'rb'),import_bookmarks=False)
    merger.append(open(tempPath + "2.pdf", 'rb'),import_bookmarks=False)
    merger.append(open(tempPath + "3.pdf", 'rb'),import_bookmarks=False)
    merger.append(open(tempPath + "4.pdf", 'rb'),import_bookmarks=False)
    merger.append(open(tempPath + "5.pdf", 'rb'),import_bookmarks=False)
    merger.append(open(content_page, 'rb'),import_bookmarks=False)
    merger.append(open(tempPath + "problems-cover.pdf", 'rb'),import_bookmarks=False)
    for puzzle_file in problem_puzzle_files:
        merger.append(open(puzzle_file, 'rb'))
    merger.append(open(tempPath + "solutions-cover.pdf", 'rb'),import_bookmarks=False)
    for puzzle_file in solution_puzzle_files:
        merger.append(open(puzzle_file, 'rb'))
    merger.append(open(tempPath + "last.pdf", 'rb'),import_bookmarks=False)
    with open(basepath + "books_output/Word Search Puzzle Book"+str(round(time()))+".pdf", "wb") as fout:
        merger.write(fout)

def generateBasePages():
    tempPath = basepath
    htmlToPDF(tempPath + "1.html", 1)
    htmlToPDF(tempPath + "2.html", 2)
    htmlToPDF(tempPath + "3.html", 3)
    htmlToPDF(tempPath + "4.html", 4)
    htmlToPDF(tempPath + "5.html", 5)
    htmlToPDF(tempPath + "problems-cover.html", "problems-cover")
    htmlToPDF(tempPath + "solutions-cover.html", "solutions-cover")
    htmlToPDF(tempPath + "last.html", "last")


class WordSearchGenerator:
    if __name__ == "__main__":
        masterList = []

        problem_puzzle_files = list()
        solution_puzzle_files = list()
        solution_puzzle_files = list()

        with open('words.yml') as f:
            puzzleSets = yaml.load_all(f, Loader=yaml.FullLoader)
            for puzzle in puzzleSets:
                puzzle_count = len(puzzle.keys())
                page_no = 9
                problem_pages = list();
                solution_pages = list();
                for title, words in puzzle.items():
                    problem_array, solution_array = fillWordGrid(words, title)

                    problem_file_path = generate_html(words, problem_array, title, page_no)
                    solution_file_path = generate_html(words, solution_array, title, (page_no + puzzle_count + 2))

                    problem_puzzle_files.append(problem_file_path)
                    solution_puzzle_files.append(solution_file_path)

                    problem_pages.append([title, page_no])
                    solution_pages.append([title, page_no + puzzle_count + 2])

                    page_no = page_no + 1

                content_page = generate_Content_page(puzzle.keys(), problem_pages, solution_pages)

        bookPages = list()
        # generateBasePages()
        printBook(problem_puzzle_files, solution_puzzle_files, content_page)
