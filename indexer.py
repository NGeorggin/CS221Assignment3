# from DEV import *
import math
import string

import nltk
import bs4
import json
import os # TODO cite os walk
import re
import time
import pickle

invertedIndex = dict()
characters = string.ascii_lowercase + string.digits

docTextHashTable = set()

fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]

#TODO stem here
#TODO Cite Stemmer https://guides.library.upenn.edu/penntdm/python/nltk
porter = nltk.stem.PorterStemmer()

######################################
for c in characters:
    file_path = os.getcwd() + "\\indices\\" + c + ".json"
    f = open(file_path, "w")
    f.write('{}')
    f.close()


j = 0
for i, subdir in enumerate(fullWalk):
    
    invertedIndex = dict()
    startTime = time.time()
    for file in subdir[2]:
      
        fileName = f".\\{subdir[0]}\\{file}"
        
        total_words = 0
        with open(fileName, "r") as fileObj:
            content = json.load(fileObj)['content']
            

            # TODO TODO Cite the hash documentation
            if hash(content) in docTextHashTable:
                print(f"Document Content with Hash {hash(content)} has already been evaluated. Skipping...")
                j += 1
                continue
            
            docTextHashTable.add(hash(content))
        
            bsObject = bs4.BeautifulSoup(content, features="html.parser")

            allHeaders = bsObject.find_all('h1') + bsObject.find_all('h2') + bsObject.find_all('h3')
            allBold = bsObject.find_all('strong') + bsObject.find_all('b')
            allTitles = bsObject.find_all('title')
            importantWords = set(" ".join([str(allHeaders), str(allBold), str(allTitles)]).lower().split(" "))

            allText = bsObject.get_text()

            wordFreq = {x.lower():0 for x in nltk.word_tokenize(allText) if re.match(r'^[a-zA-Z0-9]+$', x)}
            
            for word in nltk.word_tokenize(allText):
                total_words += 1
                if re.match(r'^[a-zA-Z0-9]+$', word):
                    wordFreq[word.lower()] += 1


            stemmedWordFreq = {}
            for token in wordFreq.keys():
                magnify = 1.1 if token in importantWords else 1

                if porter.stem(token) in stemmedWordFreq.keys():
                    stemmedWordFreq[porter.stem(token)] += (wordFreq[token] * magnify)
                else:
                    stemmedWordFreq[porter.stem(token)] = (wordFreq[token] * magnify)

                #TODO Cite Stemmer
                #TODO Check for Duplicate j values in lists see if valid

            for token in stemmedWordFreq.keys():
                """
                Since a new instance of inverted index is generated for every file, and the frequency list is stored as
                a dictionary, there cannot be more than one occurrence of a token in a given word frequency dictionary.
                TF score is generated using the word frequency divided by the total words in the document. 
                """
                if token in invertedIndex.keys():
                    invertedIndex[token].append([j, stemmedWordFreq[token] / total_words])
                else:
                    invertedIndex[token] = [[j, stemmedWordFreq[token] / total_words]]



            if j % 1000 == 0:
                print(f"{j} Webpages Writing to JSON. Rate {j*3600/(time.time()-startTime)} Webpages per Hour")

                tokenChars = {token[0] for token in invertedIndex.keys()}

                for char in tokenChars:
                    keys = [key for key in invertedIndex.keys() if key.startswith(char)]
                    if keys:
                        file_path = os.getcwd() + "\\indices\\" + char + ".json"
                        try:
                            with open(file_path, "r") as characterFile:
                                json_index = json.load(characterFile)
                        except FileNotFoundError:
                            json_index = {}

                        for key in keys:
                            if key in json_index:
                                for sublist in invertedIndex[key]:
                                    json_index[key].append(sublist)
                            else:
                                json_index[key] = []
                                for sublist in invertedIndex[key]:
                                    json_index[key].append(sublist)

                        with open(file_path, "w") as characterFile:
                            json.dump(json_index, characterFile)

                        del json_index, keys

                del invertedIndex
                invertedIndex = dict()

        j += 1
      


print(f"{j} Webpages Writing to JSON. Rate {j*3600/(time.time()-startTime)} Webpages per Hour")

tokenChars = {token[0] for token in invertedIndex.keys()}

for char in tokenChars:
    keys = [key for key in invertedIndex.keys() if key.startswith(char)]
    if keys:
        file_path = os.getcwd() + "\\indices\\" + char + ".json"
        try:
            with open(file_path, "r") as characterFile:
                json_index = json.load(characterFile)
        except FileNotFoundError:
            json_index = {}

        for key in keys:
            if key in json_index:
                for sublist in invertedIndex[key]:
                    json_index[key].append(sublist)
            else:
                json_index[key] = []
                for sublist in invertedIndex[key]:
                    json_index[key].append(sublist)

        with open(file_path, "w") as characterFile:
            json.dump(json_index, characterFile)

        del json_index, keys

del invertedIndex
invertedIndex = dict()



print("Done With TF Calculations")
####################################### TF Section ^^^





####################################### IDF Section vvv
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

    for token in json_index.keys():
        unique_words += 1
        for pairIndex in range(len(json_index[token])):
            try:
                json_index[token][pairIndex][1] = json_index[token][pairIndex][1] * math.log(file_count / len(json_index[token]))
            except:
                print(json_index[token][pairIndex])
                pass

    for token in json_index.keys():
        json_index[token] = sorted(json_index[token], key=lambda x: x[1], reverse = True)
            

    with open(file_path, "w") as characterFile:
        json.dump(json_index, characterFile)

    del json_index

    print(f"JSON Character {character} Done")


# characters = string.ascii_lowercase + string.digits

for x in characters:
    with open(os.getcwd() + "\\indices\\" + x + ".json", "r") as json_file:
        data = json.load(json_file)

    with open(os.getcwd() + "\\indices_pickle\\" + x + ".pkl", "wb") as pickle_file:
        pickle.dump(data, pickle_file)

    print(f"PKL Character {x} Done")

print("Done With IDF Calculations")

print("Unique tokens: " + str(unique_words))

#######################################