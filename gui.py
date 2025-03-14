import tkinter as tk
from search import search

import json, os

# TODO TODO Cite https://cs.gmu.edu/~dfleck/classes/cs112/spring08/slides/tkinter.pdf
# TODO TODO maybe cite the actual docs

def searchGUI():

    resultList, elapsedTime = search(searchQuery.get())


    if resultList == []:
        urlLabel = tk.Label(root, text=f"Query Results:\nNo Results Found.\n\nTime Elapsed: {elapsedTime} milliseconds.\n", bg="light blue")
        urlLabel.pack()
    else:
        print(resultList)
        urlLabel = tk.Label(root, text=f"Query Results:\n" + ("\n".join([docMapping[str(docid)][1] for docid in resultList])) + f"\n\nTime Elapsed: {elapsedTime} milliseconds.\n", bg="light blue")
        urlLabel.pack()

with open(os.getcwd() + "\\documentHashmap.json", "r") as documentHashmap:
    docMapping = json.load(documentHashmap)


root = tk.Tk()

label = tk.Label(root, text="SWE 225 / CS 221 Assignment 3\nGraphical User Interface\n")
label.pack()

searchQuery = tk.Entry(root,width=40)
searchQuery.pack()

searchButton = tk.Button(root, text="Execute Query", command=searchGUI)
searchButton.pack()

root.mainloop()