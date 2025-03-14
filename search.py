import os
import json
import pickle
import time
import heapq
from concurrent.futures import ThreadPoolExecutor
from itertools import islice

import nltk
from collections import Counter

with open(os.getcwd() + "\\documentHashmap.json", "r") as documentHashmap:
    docMapping = json.load(documentHashmap)

# TODO stem here
# TODO Cite Stemmer https://guides.library.upenn.edu/penntdm/python/nltk
porter = nltk.stem.PorterStemmer()

while True:
    searchQueryString = input("Search Query: ")
    startTime = time.time()

    searchQueryList = set([porter.stem(word) for word in searchQueryString.split()])

    if len(searchQueryList) > 1:
        res = []

        for word in searchQueryList:
            with open(os.getcwd() + f"\\indices_pickle\\{word[0].lower()}.pkl", "rb") as jsonQuery:
                try:
                    res.append(dict(pickle.load(jsonQuery)[word.lower()]))
                except KeyError:
                    pass
                except FileNotFoundError:
                    print("Invalid query.")

        if not res:
            print("No results found.")

        elif len(res) == 1:
            print("Short search")
            exact_query_scores = list(islice(res[0].keys(), 5))

            for i in range(len(exact_query_scores)):
                print(f"Page {i + 1}: {docMapping[str(exact_query_scores[i])][1]}")

        else:

            # keys = [set(x.keys()) for x in res[:1]]
            # query_keys = [[val for val in res[0] if val in y] for y in keys][0]
            # query_keys = set(res[0]).intersection(*res[1:])

            query_keys = set(min(res, key=lambda x: len(x.keys()), default={}).keys())
            for r in res:
                query_keys.intersection_update(r.keys())

            # for d in res:
            #     if len(d) > len(query_keys):
            #         res.remove(d)

            query_dict = {k: sum([y[k] for y in res]) for k in query_keys}
            # query_dict = Counter()
            # for d in res:
            #     query_dict.update(d)

            query_result = heapq.nlargest(5, query_keys, key=query_dict.get)
            # query_result = sorted(list(query_dict.keys()), key=lambda x: query_dict[x], reverse=True)[:5]
            # exact_query_scores = {}
            # pointer = 0
            #
            # exact_match_documents = list(set(res[0]).intersection(*res[1:]))
            #
            # while pointer < len(exact_match_documents) and len(exact_query_scores) < 5:
            #     score = 0
            #     document = exact_match_documents[pointer]
            #
            #     for term in res:
            #         score += term.get(document)
            #     exact_query_scores[document] = score
            #
            #     pointer += 1
            #
            # exact_query_scores = list(exact_query_scores.keys())
            # exact_query_scores = sorted(list(exact_query_scores.keys()), key=lambda x: exact_query_scores[x], reverse=True)[
            #                      :5]

            for i in range(len(query_result)):
                print(f"Page {i + 1}: {docMapping[str(query_result[i])][1]}")

            if len(query_result) < 5:

                print("Executing Fuzzy Scores")
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

                fuzzy_scores = sorted(fuzzy_scores.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True)[
                               :5 - len(query_result)]

                for i in range(len(fuzzy_scores)):
                    print(f"Page {i + len(query_result) + 1}: {docMapping[str(fuzzy_scores[i][0])][1]}")


    else:
        try:
            with open(os.getcwd() + f"\\indices\\{searchQueryString[0].lower()}.json", "r") as jsonQuery:

                    exact_query_scores = json.load(jsonQuery)[porter.stem(searchQueryString.lower())][:5]

                    for i in range(len(exact_query_scores)):
                        print(f"Page {i + 1}: {docMapping[str(exact_query_scores[i][0])][1]}, {docMapping[str(exact_query_scores[i][0])]}")

        except FileNotFoundError:
            print("Invalid query.")
        except KeyError:
            print("No results found.")
            ## TODO TODO similarity
            # print(exact_query_scores)

    print(f"Time Elapsed: {int(1000 * (time.time() - startTime))} milliseconds")

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
