# from DEV import *
import nltk
import bs4
import json
import os # TODO cite os walk

invertedIndex = dict()

# with open("invertedIndex.txt", "a+") as invertedIndexFile:

# for folder in :
#     for page in folder: 
#         with open(page, "r") as pageFile:
#             content = json.load(pageFile)

# content = json.load(open(".\\DEV\\alderis_ics_uci_edu\\0f274aaa945c05641a9677b951c32026bb201ec9aeb6e691fedd1235b3a5d6af.json"))
# print(content)

fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]
for subdir in fullWalk:
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
            
            

# Beautiful Soup It

# Create Data Structures

# SOMEHOW compute tf-idf for each

# Return Final