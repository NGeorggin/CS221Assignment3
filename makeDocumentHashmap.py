import os
import json

# Make a document hashmap that assigns docids to pairings of DEV file names and the url that the page refers to.
# Preprocessed now so it can be easily loaded later

# OS Walk to cycle through all folders and files in DEV functionality from (Matloff, 2009).
fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]
 
# Init variables to hold document information
docMapping = dict()
j = 0

# OS Walk to cycle through all folders and files in DEV functionality from (Matloff, 2009).
# Cycle through the files in DEV
for i, subdir in enumerate(fullWalk):
    for file in subdir[2]:
        
        if j % 1000 == 0:
            print(f"{j} Webpages Evaluated")
            # print(docMapping)

        # Make it so a docid number is paired with a DEV file path
        docMapping[j] = [subdir[0] + "\\" + file]

        # Open that file and add the url from that page to the list in the dictionary value
        with open(os.getcwd() + docMapping[j][0], "r") as htmlFile:
            docMapping[j].append(json.load(htmlFile)['url'])

        j += 1 # Increment the docid numbers

# Write all this to a JSON file
with open(os.getcwd() + "\\documentHashmap.json", "w") as documentHashmap:
    json.dump(docMapping, documentHashmap)

# Reference(s):
# Matloff, N. (2009). Tutorial on File and Directory Access in Python. University of California, Davis. https://heather.cs.ucdavis.edu/matloff/public_html/Python/PyFileDir.pdf