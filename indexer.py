import math
import string
import nltk
import bs4
import json
import os
import re
import time
import pickle

invertedIndex = dict()
characters = string.ascii_lowercase + string.digits

docTextHashTable = set()

# OS Walk to cycle through all folders and files in DEV functionality from (Matloff, 2009).
fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]

# Porter Stemmer from (NLTK Package, 2024).
porter = nltk.stem.PorterStemmer()

# Making a json file for each of the characters and digits in our scope
for c in characters:
    file_path = os.getcwd() + "\\indices\\" + c + ".json"
    f = open(file_path, "w")
    f.write('{}')
    f.close()


j = 0 # Counting the number of files in DEV

# Init the inverted index
invertedIndex = dict() 
startTime = time.time()

# OS Walk to cycle through all folders and files in DEV functionality from (Matloff, 2009).
# Cycle through the files in DEV
for i, subdir in enumerate(fullWalk):
    for file in subdir[2]:
      
        # Get the file from DEV
        fileName = f".\\{subdir[0]}\\{file}"
        
        total_words = 0
        with open(fileName, "r") as fileObj:

            # Load the content from that webpage
            content = json.load(fileObj)['content']
            
            # Python built-in hash functionality from (Hashing and Dictionaries, 2019).
            # Pass over the duplicate page
            if hash(content) in docTextHashTable:
                print(f"Document Content with Hash {hash(content)} has already been evaluated. Skipping...")
                j += 1
                continue
            
            # Python built-in hash functionality from (Hashing and Dictionaries, 2019).
            docTextHashTable.add(hash(content))
        
            # Make a BeautifulSoup object of it
            bsObject = bs4.BeautifulSoup(content, features="html.parser")

            # Making a set of words which are in the headers, titles, boldface, etc.
            allHeaders = bsObject.find_all('h1') + bsObject.find_all('h2') + bsObject.find_all('h3')
            allBold = bsObject.find_all('strong') + bsObject.find_all('b')
            allTitles = bsObject.find_all('title')
            importantWords = set(" ".join([str(allHeaders), str(allBold), str(allTitles)]).lower().split(" "))

            # Get the text from the BeautifulSoup object and tokenize it with NLTK
            allText = bsObject.get_text()
            wordFreq = {x.lower():0 for x in nltk.word_tokenize(allText) if re.match(r'^[a-zA-Z0-9]+$', x)}
            
            # Count the word frequency from the page if they are proper alphanumerics
            for word in nltk.word_tokenize(allText):
                total_words += 1
                if re.match(r'^[a-zA-Z0-9]+$', word):
                    wordFreq[word.lower()] += 1


            # Make a new dictionary to hold the stemmed tokens
            stemmedWordFreq = {}
            for token in wordFreq.keys():

                # Add a small multiplier if the word in question appears in the headers or bold
                magnify = 1.1 if token in importantWords else 1

                # Porter Stemmer Implementation from (NLTK Package, 2024).
                if porter.stem(token) in stemmedWordFreq.keys():
                    stemmedWordFreq[porter.stem(token)] += (wordFreq[token] * magnify)
                else:
                    stemmedWordFreq[porter.stem(token)] = (wordFreq[token] * magnify)

            # Finish the TF Calculation and add to inverted index
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


            # Every 1000 pages to find balance in space/runtime tradeoffs
            if j % 1000 == 0:
                print(f"{j} Webpages Writing to JSON. Rate {j*3600/(time.time()-startTime)} Webpages per Hour")

                # For each unique token starting character
                tokenChars = {token[0] for token in invertedIndex.keys()}
                for char in tokenChars:
                    keys = [key for key in invertedIndex.keys() if key.startswith(char)]
                    if keys:
                        # Open up that json file
                        file_path = os.getcwd() + "\\indices\\" + char + ".json"
                        try:
                            with open(file_path, "r") as characterFile:
                                json_index = json.load(characterFile)
                        except FileNotFoundError:
                            json_index = {}

                        # Add the inverted index to the JSON Dictionary
                        for key in keys:
                            if key in json_index:
                                for sublist in invertedIndex[key]:
                                    json_index[key].append(sublist)
                            else:
                                json_index[key] = []
                                for sublist in invertedIndex[key]:
                                    json_index[key].append(sublist)

                        # Write it to the JSON Files
                        with open(file_path, "w") as characterFile:
                            json.dump(json_index, characterFile)

                        # Reset the appropriate variables to wisely use space
                        del json_index, keys

                del invertedIndex
                invertedIndex = dict()

        j += 1 # Increment File Counter
      

# At the end of the scan...
print(f"{j} Webpages Writing to JSON. Rate {j*3600/(time.time()-startTime)} Webpages per Hour")

# For each unique token starting character
tokenChars = {token[0] for token in invertedIndex.keys()}
for char in tokenChars:
    keys = [key for key in invertedIndex.keys() if key.startswith(char)]
    if keys:
        # Open up that json file
        file_path = os.getcwd() + "\\indices\\" + char + ".json"
        try:
            with open(file_path, "r") as characterFile:
                json_index = json.load(characterFile)
        except FileNotFoundError:
            json_index = {}

        # Add the inverted index to the JSON Dictionary   
        for key in keys:
            if key in json_index:
                for sublist in invertedIndex[key]:
                    json_index[key].append(sublist)
            else:
                json_index[key] = []
                for sublist in invertedIndex[key]:
                    json_index[key].append(sublist)

        # Write it to the JSON Files
        with open(file_path, "w") as characterFile:
            json.dump(json_index, characterFile)

        # Reset the appropriate variables to wisely use space
        del json_index, keys

del invertedIndex
invertedIndex = dict()

print("Done With TF Calculations")

# Count the files in DEV
unique_words = 0

# OS Walk to cycle through all folders and files in DEV functionality from (Matloff, 2009).
file_count = sum(len(files) for _, _, files in os.walk('.\\DEV'))

print("File Count: " + str(file_count))

# For each of the JSON files denoted by a character
for character in characters:
    # Open the file and get the dictionary
    file_path = os.getcwd() + "\\indices\\" + character + ".json"
    try:
        with open(file_path, "r") as characterFile:
            json_index = json.load(characterFile)
    except FileNotFoundError:
        json_index = {}

    # Complete the IDF Calculation for each token
    for token in json_index.keys():
        unique_words += 1
        for pairIndex in range(len(json_index[token])):
            try:
                json_index[token][pairIndex][1] = json_index[token][pairIndex][1] * math.log(file_count / len(json_index[token]))
            except:
                print(json_index[token][pairIndex])
                pass

    # Sort the list from highest to lowest TF-IDF score
    for token in json_index.keys():
        json_index[token] = sorted(json_index[token], key=lambda x: x[1], reverse = True)
            
    # Write the updated dictionary back to the file
    with open(file_path, "w") as characterFile:
        json.dump(json_index, characterFile)

    del json_index

    print(f"JSON Character {character} Done")

# Make a copy of the JSON file into a PKL Format and store them for quicker access during search
for x in characters:
    with open(os.getcwd() + "\\indices\\" + x + ".json", "r") as json_file:
        data = json.load(json_file)

    with open(os.getcwd() + "\\indices_pickle\\" + x + ".pkl", "wb") as pickle_file:
        pickle.dump(data, pickle_file)

    print(f"PKL Character {x} Done")

print("Done With IDF Calculations")

print("Unique tokens: " + str(unique_words))


# Reference(s):
# Hashing and Dictionaries. (2019). Carnegie Mellon University. https://www.cs.cmu.edu/~15110-f19/slides/week8-1-hashing.pdf
# Matloff, N. (2009). Tutorial on File and Directory Access in Python. University of California, Davis. https://heather.cs.ucdavis.edu/matloff/public_html/Python/PyFileDir.pdf
# NLTK Package. (2024). University of Pennsylvania. https://guides.library.upenn.edu/penntdm/python/nltk