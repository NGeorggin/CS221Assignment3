import json
import os
import tkinter as tk
from search import search

# Function to be executed upon button press
def searchGUI():

    # Call the function from search.py to get the best five webpages and the total elapsed time
    resultList, elapsedTime = search(searchQuery.get())

    if resultList == []: # If no returns, then say no results
        # Label and Packing Operation on Tkinter from (Fleck, 2008, p. 4)
        urlLabel = tk.Label(root, text=f"Query Results:\nNo Results Found.\n\nTime Elapsed: {elapsedTime} milliseconds.\n", bg="light blue")
        urlLabel.pack()

    else: # If there are returns, then print them
        # Label and Packing Operation on Tkinter from (Fleck, 2008, p. 4)
        urlLabel = tk.Label(root, text=f"Query Results:\n" + ("\n".join([docMapping[str(docid)][1] for docid in resultList])) + f"\n\nTime Elapsed: {elapsedTime} milliseconds.\n", bg="light blue")
        urlLabel.pack()

# Loading the preprocessed document hashmap from memory so we can easily access it later
with open(os.getcwd() + "\\documentHashmap.json", "r") as documentHashmap:
    docMapping = json.load(documentHashmap)

# Tkinter root operations from (Fleck, 2008, p. 4)
root = tk.Tk()

# Label and Packing Operation on Tkinter from (Fleck, 2008, p. 4)
label = tk.Label(root, text="SWE 225 / CS 221 Assignment 3\nGraphical User Interface\n")
label.pack()

# Entry and Packing Operation on Tkinter from (Fleck, 2008, p. 13)
searchQuery = tk.Entry(root,width=40)
searchQuery.pack()

# Button (with function and text) and Packing Operation on Tkinter from (Fleck, 2008, p. 11)
searchButton = tk.Button(root, text="Execute Query", command=searchGUI)
searchButton.pack()

# Tkinter root operations from (Fleck, 2008, p. 4)
root.mainloop()


# Reference(s):
# Fleck, D. (2008). Tkinter - GUIs in Python. George Mason University. https://cs.gmu.edu/~dfleck/classes/cs112/spring08/slides/tkinter.pdf