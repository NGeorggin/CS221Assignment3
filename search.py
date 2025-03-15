import os
import pickle
import time
import heapq
import nltk
from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from collections import Counter


def search(searchQueryString):

    startTime = time.time()

    returnableList = []

    # Porter Stemmer from (NLTK Package, 2024).
    porter = nltk.stem.PorterStemmer()
    
    # Porter Stemmer Implementation from (NLTK Package, 2024).
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

            returnableList = exact_query_scores
            print("Case 1:", returnableList)


        else:

            query_keys = set(min(res, key=lambda x: len(x.keys()), default={}).keys())
            for r in res:
                query_keys.intersection_update(r.keys())

            query_dict = {k: sum([y[k] for y in res]) for k in query_keys}

            query_result = heapq.nlargest(5, query_keys, key=query_dict.get)

            
            returnableList = query_result
            print("Case 2:", returnableList)


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

                fuzzy_scores = sorted(fuzzy_scores.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True)[:5 - len(query_result)]

                returnableList += [item[0] for item in fuzzy_scores]
                print("Case 3:", returnableList)


    else:
        try:
            with open(os.getcwd() + f"\\indices_pickle\\{searchQueryString[0].lower()}.pkl", "rb") as jsonQuery:

                    # Porter Stemmer Implementation from (NLTK Package, 2024).
                    exact_query_scores = pickle.load(jsonQuery)[porter.stem(searchQueryString.lower())][:5]

                    returnableList = [docid[0] for docid in exact_query_scores]
                    print("Case 4:", returnableList)


        except FileNotFoundError:
            print("Invalid query.")
        except KeyError:
            print("No results found.")

    endTime = time.time()

    return returnableList, int(1000*(endTime-startTime))



# Reference(s):
# NLTK Package (2024). University of Pennsylvania. https://guides.library.upenn.edu/penntdm/python/nltk