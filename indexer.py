# from DEV import *
import nltk
import bs4
import json
import os # TODO cite os walk
import re

invertedIndex = dict()

# with open("invertedIndex.txt", "a+") as invertedIndexFile:

# for folder in :
#     for page in folder: 
#         with open(page, "r") as pageFile:
#             content = json.load(pageFile)

# content = json.load(open(".\\DEV\\alderis_ics_uci_edu\\0f274aaa945c05641a9677b951c32026bb201ec9aeb6e691fedd1235b3a5d6af.json"))
# print(content)

# key=t, val=[Posting(docid, tf)]
class Posting:
    def __init__(self, docid, tf):
        self.docid = docid
        self.tf = tf
    def __repr__(self):
        return f"Posting(docid={self.docid},tf={self.tf})"

invertedIndex = dict()

fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]
for i, subdir in enumerate(fullWalk):
    print(subdir)
    for file in subdir[2]:
        fileName = f".\\{subdir[0]}\\{file}"
        with open(fileName, "r") as fileObj:
            content = json.load(fileObj)['content']
            bsObject = bs4.BeautifulSoup(content)
            allHeaders = bsObject.find_all('h1') + bsObject.find_all('h2') + bsObject.find_all('h3')
            allBold = bsObject.find_all('strong') + bsObject.find_all('b')
            allTitles = bsObject.find_all('title') # TODO Check
            
            allText = bsObject.get_text()
            ## TOKENIZE THE TEXT FROM Assignment 2
            wordFreq = {x.lower():0 for x in nltk.word_tokenize(allText) if re.match(r"^[a-zA-Z0-9]+$", x)}
            for word in nltk.word_tokenize(allText):
                if re.match(r"^[a-zA-Z0-9]+$", word):
                    wordFreq[word.lower()] += 1
            # Go through each token and record frequency from part 1 code and get tf from that

            for token in wordFreq.keys():
                ## CALCULATE TF
                if token not in invertedIndex:
                    invertedIndex[token] = [Posting(i, wordFreq[token])]
                else:
                    invertedIndex[token].append(Posting(i, wordFreq[token]))

            # print(invertedIndex)
        if len(invertedIndex) > 10000:
            break
    if len(invertedIndex) > 10000:
        break
    #     break
    # break


print(invertedIndex)

            
            

# Beautiful Soup It

# Create Data Structures

# SOMEHOW compute tf-idf for each

# Return Final