# from DEV import *
import math
import string

import nltk
import bs4
import json
import os # TODO cite os walk
import re

invertedIndex = dict()
characters = string.ascii_lowercase + string.digits

for c in characters:
    file_path = os.getcwd() + "\\indices\\" + c + ".json"
    f = open(file_path, "w")
    f.write('{}')
    f.close()

# with open("invertedIndex.txt", "a+") as invertedIndexFile:

# for folder in :
#     for page in folder: 
#         with open(page, "r") as pageFile:
#             content = json.load(pageFile)

# content = json.load(open(".\\DEV\\alderis_ics_uci_edu\\0f274aaa945c05641a9677b951c32026bb201ec9aeb6e691fedd1235b3a5d6af.json"))
# print(content)

# key=t, val=[Posting(docid, tf)]

class Posting():
    def __init__(self, docid, tf):
        self.docid = docid
        self.tf = tf
    def __repr__(self):
        return f"Posting(docid={self.docid},tf={self.tf})"

    def get_tf(self):
        return self.tf

    def get_id(self):
        return self.docid

    def set_tf(self, tf):
        self.tf = tf


def json_combine(key_list: list, new_index: dict, disk_index: dict) -> dict:
    for key in key_list:
        if key in disk_index:
            disk_index[key].append((new_index[key].get_id(), new_index[key].get_tf()))
        else:
            disk_index[key] = [(new_index[key].get_id(), new_index[key].get_tf())]

    return disk_index


fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]

docMapping = dict()
for i, subdir in enumerate(fullWalk):
    # print(subdir)
    for file in subdir[2]:
        # print(file)
        fileStringName = re.match(r'[a-zA-Z0-9]+', file).group()
        docMapping[fileStringName] = i

for i, subdir in enumerate(fullWalk):
    print(subdir)
    for file in subdir[2]:
        fileName = f".\\{subdir[0]}\\{file}"
        invertedIndex = dict()

        total_words = 0
        with open(fileName, "r") as fileObj:
            content = json.load(fileObj)['content']
            bsObject = bs4.BeautifulSoup(content, features="html.parser")
            allHeaders = bsObject.find_all('h1') + bsObject.find_all('h2') + bsObject.find_all('h3')
            allBold = bsObject.find_all('strong') + bsObject.find_all('b')
            allTitles = bsObject.find_all('title') # TODO Check
            
            allText = bsObject.get_text()
            ## TOKENIZE THE TEXT FROM Assignment 2
            wordFreq = {x.lower():0 for x in nltk.word_tokenize(allText) if re.match(r"^[a-zA-Z0-9]+$", x)}
            for word in nltk.word_tokenize(allText):
                total_words += 1
                if re.match(r"^[a-zA-Z0-9]+$", word):
                    wordFreq[word.lower()] += 1
            # Go through each token and record frequency from part 1 code and get tf from that

            for token in wordFreq.keys():
                """
                Since a new instance of inverted index is generated for every file, and the frequency list is stored as
                a dictionary, there cannot be more than one occurrence of a token in a given word frequency dictionary.
                TF score is generated using the word frequency divided by the total words in the document. 
                """
                invertedIndex[token] = Posting(docMapping[re.match(r'[a-zA-Z0-9]+', file).group()], wordFreq[token] / total_words)

            for char in characters:
                keys = [key for key in invertedIndex.keys() if key.startswith(char)]

                if keys:
                    file_path = os.getcwd() + "\\indices\\" + char + ".json"

                    try:
                        with open(file_path, "r") as characterFile:
                            json_index = json.load(characterFile)
                    except FileNotFoundError:
                        json_index = {}

                    combined_index = json_combine(keys, invertedIndex, json_index)
                    with open(file_path, "w") as characterFile:
                        json.dump(combined_index, characterFile)


unique_words = 0
file_count = sum(len(files) for _, _, files in os.walk('.\\DEV'))

print("File Count: " + str(file_count))

for character in characters:
    file_path = os.getcwd() + "\\indices\\" + character + ".json"
    try:
        with open(file_path, "r") as characterFile:
            json_index = json.load(characterFile)
    except FileNotFoundError:
        json_index = {}

    for token in json_index:
        unique_words += 1
        for instance in json_index[token]:
            instance[1] = instance[1] * math.log(file_count / len(json_index[token]))

    with open(file_path, "w") as characterFile:
        json.dump(json_index, characterFile)

print("Unique tokens: " + str(unique_words))

# Beautiful Soup It

# Create Data Structures

# SOMEHOW compute tf-idf for each

# Return Final