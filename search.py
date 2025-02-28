# import os, re, json

# fullWalk = [i for i in os.walk(".\\DEV") if len(i[1]) == 0]

# docMapping = dict()
# j = 0
# for i, subdir in enumerate(fullWalk):
#     # print(subdir)
#     for file in subdir[2]:
#         # print(file)
#         fileStringName = re.match(r'[a-zA-Z0-9]+', file).group()
#         docMapping[fileStringName] = j
#         j += 1

# with open(os.getcwd() + "\\documentHashmap.json", "w") as fileObj:
#     json.dump(docMapping,fileObj) 