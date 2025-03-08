import heapq
import os
import json
import pickle
import string
import time
from collections import defaultdict, Counter

with open(os.getcwd() + "\\documentHashmap.json", "r") as documentHashmap:
    docMapping = json.load(documentHashmap)

while True:
    # TODO: clean/sanitise input
    searchQueryString = input("Search Query: ")
    startTime = time.time()

    searchQueryList = searchQueryString.split()

    if len(searchQueryList) > 1:
        res = []

        for word in searchQueryList:
            with open(os.getcwd() + f"\\indices_pickle\\{word.lower()[0]}.pkl", "rb") as jsonQuery:
                pickle_index = pickle.load(jsonQuery)
                index = dict(pickle_index[word.lower()])
                res.append(index)

        exact_match_documents = set(res[0].keys())
        for term_dict in res[1:]:
            exact_match_documents &= set(term_dict.keys())

        exact_query_scores = {}
        for document in exact_match_documents:
            score = 0
            for term in res:
                score += term.get(document)
            exact_query_scores[document] = score

        exact_query_scores = sorted(list(exact_query_scores.keys()), key = lambda x: exact_query_scores[x], reverse = True)[:5]

        for i in range(len(exact_query_scores)):
            print(f"Page {i + 1}: {docMapping[str(exact_query_scores[i])][1]}, {docMapping[str(exact_query_scores[i])]}")
        if len(exact_query_scores) < 5:
            fuzzy_scores = {}

            term_count = Counter()
            for d in res:
                term_count.update(d.keys())

            for doc, count in term_count.items():
                score = 0
                for term in res:
                    if term.get(doc):
                        score += term.get(doc)
                fuzzy_scores[doc] = (count, score)

            fuzzy_scores = sorted(fuzzy_scores.items(), key=lambda item: (item[1][1], item[1][0]))[:5-len(exact_query_scores)]

            for i in range(len(fuzzy_scores)):
                print(f"Page {i + len(exact_query_scores)}: {docMapping[str(fuzzy_scores[i][0])][1]}, {docMapping[str(fuzzy_scores[i][0])]}")

        # master of software engineering
        # if len(exact_query_scores) < 5:
        #     for i in range(len(exact_query_scores)):
        #         print(f"Page {i + 1}: {docMapping[str(exact_query_scores[i])][1]}")
        #
        # else:
        #     for i in range(5):
        #         print(f"Page {i + 1}: {docMapping[str(exact_query_scores[i])][1]}")



    else:
        with open(os.getcwd() + f"\\indices\\{searchQueryString.lower()[0]}.json", "r") as jsonQuery:
            # TODO implement similarity
            exact_query_scores = json.load(jsonQuery)[searchQueryString.lower()]
            # print(len(exact_query_scores))
            exact_query_scores = sorted(exact_query_scores, key = lambda x: x[1], reverse = True)
            if len(exact_query_scores) < 5:
                for i in range(len(exact_query_scores)):
                    print(f"Page {i + 1}: {docMapping[str(exact_query_scores[i][0])][1]}")

                ## TODO TODO full 5 options
                # print(exact_query_scores)
            else:
                for i in range(5):
                    print(f"Page {i + 1}: {docMapping[str(exact_query_scores[i][0])][1]}")
                # print(exact_query_scores[:5])

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

######################################

# import json
# import pickle
# import string
# import os

# characters = string.ascii_lowercase + string.digits

# for x in characters:
#     with open(os.getcwd() + "\\indices\\" + x + ".json", "r") as json_file:
#         data = json.load(json_file)

#     with open(os.getcwd() + "\\indices_pickle\\" + x + ".pkl", "wb") as pickle_file:
#         pickle.dump(data, pickle_file)

# print("pickle!")