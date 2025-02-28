import os
import json

searchQueryString = input("Search Query: ")
searchQueryList = searchQueryString.split()

if len(searchQueryList) > 1:
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