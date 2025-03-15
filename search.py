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
    # Stem each incoming word
    searchQueryList = set([porter.stem(word) for word in searchQueryString.split()])

    if len(searchQueryList) > 1: # If it is a multiword query
        res = []

        for word in searchQueryList:
            # Open the file corresponding to each word in the query
            with open(os.getcwd() + f"\\indices_pickle\\{word[0].lower()}.pkl", "rb") as jsonQuery:
                try:
                    # Get the posting lists from that file
                    res.append(dict(pickle.load(jsonQuery)[word.lower()]))
                
                # Appropriate error checking
                except KeyError:
                    pass
                except FileNotFoundError:
                    print("Invalid query.")

        # Case for no results found
        if not res:
            print("No results found.")

        # Case for if one word is valid and the rest are not
        elif len(res) == 1:
            print("Short search")
            exact_query_scores = list(islice(res[0].keys(), 5))

            returnableList = exact_query_scores
            print("Case 1:", returnableList)


        else:

            # Use set intersection logic to find docs that contain all of the terms (AND boolean functionality)
            query_keys = set(min(res, key=lambda x: len(x.keys()), default={}).keys())
            for r in res:
                query_keys.intersection_update(r.keys())

            query_dict = {k: sum([y[k] for y in res]) for k in query_keys}

            # Give us the five highest scoring such documents
            query_result = heapq.nlargest(5, query_keys, key=query_dict.get)

            
            returnableList = query_result
            print("Case 2:", returnableList)


            if len(query_result) < 5: # If this gives us too few pages

                print("Executing Fuzzy Scores")
                fuzzy_scores = {}

                # Count how many more documents we need to complete the query
                term_count = Counter()
                for d in res:
                    term_count.update(d.keys())

                # Use set union logic to find docs that contain at least one of the terms (OR boolean functionality)
                for doc, count in term_count.items():
                    score = 0
                    for term in res:
                        if term.get(doc):
                            score += term.get(doc)
                    fuzzy_scores[doc] = (count, score)

                # Update these docids with the docids from the previous subsection
                fuzzy_scores = sorted(fuzzy_scores.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True)[:5 - len(query_result)]

                returnableList += [item[0] for item in fuzzy_scores]
                print("Case 3:", returnableList)


    else: # If it is a one word query
        try:
            # Open the PKL file with that word
            with open(os.getcwd() + f"\\indices_pickle\\{searchQueryString[0].lower()}.pkl", "rb") as jsonQuery:

                    # Porter Stemmer Implementation from (NLTK Package, 2024).
                    # Get the top five docs from the list in the index after stemming term
                    exact_query_scores = pickle.load(jsonQuery)[porter.stem(searchQueryString.lower())][:5]

                    # Extract the docid numbers and send to GUI
                    returnableList = [docid[0] for docid in exact_query_scores]
                    print("Case 4:", returnableList)

        # Appropriate error checking
        except FileNotFoundError:
            print("Invalid query.")
        except KeyError:
            print("No results found.")

    endTime = time.time()

    # Return the list of docids and total time elapsed in milliseconds
    return returnableList, int(1000*(endTime-startTime))



# Reference(s):
# NLTK Package (2024). University of Pennsylvania. https://guides.library.upenn.edu/penntdm/python/nltk