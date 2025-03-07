import os
import json
import time

with open(os.getcwd() + "\\documentHashmap.json", "r") as documentHashmap:
    docMapping = json.load(documentHashmap)

searchQueryString = input("Search Query: ")
startTime = time.time()

searchQueryList = searchQueryString.split()
if len(searchQueryList) > 1:
    
    docDictionary = dict()
    for word in searchQueryList:
        with open(os.getcwd() + f"\\indices\\{word[0].lower()}.json", "r") as jsonQuery:
            for docid, tfidf in json.load(jsonQuery)[word.lower()]:
                if docid in docDictionary:
                    docDictionary[docid] += tfidf
                else:
                    docDictionary[docid] = tfidf
            
            del jsonQuery
            
    queryScores = sorted(list(docDictionary.keys()), key = lambda x: docDictionary[x], reverse = True)
    if len(queryScores) < 5:
        for i in range(len(queryScores)):
            print(f"Page {i + 1}: {docMapping[str(queryScores[i])][1]}")

    else:
        for i in range(5):
            print(f"Page {i + 1}: {docMapping[str(queryScores[i])][1]}")



else:
    with open(os.getcwd() + f"\\indices\\{searchQueryString[0].lower()}.json", "r") as jsonQuery:
        # TODO implement similarity
        queryScores = json.load(jsonQuery)[searchQueryString.lower()]
        queryScores = sorted(queryScores, key = lambda x: x[1], reverse = True)
        if len(queryScores) < 5:
            for i in range(len(queryScores)):
                print(f"Page {i + 1}: {docMapping[str(queryScores[i][0])][1]}")

            ## TODO TODO full 5 options
            # print(queryScores)
        else:
            for i in range(5):
                print(f"Page {i + 1}: {docMapping[str(queryScores[i][0])][1]}")
            # print(queryScores[:5])

print(f"Time Elapsed: {int(1000*(time.time() - startTime))} milliseconds")


#########################################

# import os,json

# fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]

# docMapping = dict()
# j = 0
# for i, subdir in enumerate(fullWalk):
#     for file in subdir[2]:
        
#         if j % 1000 == 0:
#             print(f"{j} Webpages Evaluated")
#             # print(docMapping)

#         docMapping[j] = [subdir[0] + "\\" + file]

#         with open(os.getcwd() + docMapping[j][0], "r") as htmlFile:
#             docMapping[j].append(json.load(htmlFile)['url'])

#         j += 1


# with open(os.getcwd() + "\\documentHashmap.json", "w") as documentHashmap:
#     json.dump(docMapping, documentHashmap)