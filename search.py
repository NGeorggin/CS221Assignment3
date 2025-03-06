import os
import json
import time

searchQueryString = input("Search Query: ")
startTime = time.time()

searchQueryList = searchQueryString.split()
if len(searchQueryList) > 1:
    wordDatabase = dict()
    for word in searchQueryList:
        with open(os.getcwd() + f"\\indices\\{word.lower()[0]}.json", "r") as jsonQuery:
            wordDatabase[word.lower()] = sorted(json.load(jsonQuery)[word.lower()], key = lambda x: x[1], reverse = True)
            del jsonQuery
            ## TODO set intersection logic
    print(wordDatabase)
    pass
else:
    with open(os.getcwd() + f"\\indices\\{searchQueryString[0]}.json", "r") as jsonQuery:
        # TODO implement similarity
        queryScores = json.load(jsonQuery)[searchQueryString]
        queryScores = sorted(queryScores, key = lambda x: x[1], reverse = True)
        if len(queryScores) <= 5:
            print(queryScores)
        else:
            print(queryScores[:5])

print(f"Time Elapsed: {int(1000*(time.time() - startTime))} milliseconds")
