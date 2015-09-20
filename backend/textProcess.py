
from nltk.corpus import words
# d = enchant.Dict("en_US")


# splits a file into lines, and then takes each word from a line and compares it
# to real english lexicon dictionary. After the comparison a string of real
# words is returned
def textParse(file):
    processedText = ''
    with open(file, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            wordsInLine = line.split(' ')
            for word in wordsInLine:
                # print '*'+word+'*'
                if word.lower() in words.words():
                    processedText += word + ' '
    return processedText


# print "hello" in words.words()
processText = textParse('output.txt')
# print processText
