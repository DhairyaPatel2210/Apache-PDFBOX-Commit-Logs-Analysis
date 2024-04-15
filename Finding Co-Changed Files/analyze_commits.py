from collections import defaultdict
from itertools import combinations

import json

import pandas as pd
# Opening JSON file
f = open('commit_data.json')
#below num_files can be changed to 3,4,5 and reran the same program creating all 3 different csv's
num_files=5
# returns JSON object as 
# a dictionary
commit_files = json.load(f)
commit_files=list(commit_files.items())
commit_files=sorted(commit_files,key=lambda x:x[0])
total_files=set()
for commit,files in commit_files:
    for file in files:
        total_files.add(file)
total_files=list(total_files)
#sort files according to alphabetical order
total_files=sorted(total_files)
co_changed_files = defaultdict(list)
#below if sliding window of num_files as length of window
for i in range(0,len(total_files),num_files):
    cur_files=[]
    if i+num_files>=len(total_files):
        break
    for index in range(i,i+num_files):
        cur_files.append(total_files[index])
    for commit,files in commit_files:
        files=set(files)
        flag=True 
        for file in cur_files:
            if file not in files:
                flag=False 
        if(flag):
            co_changed_files[tuple(cur_files)].append(commit)

filtered_sets=[]
for tup in co_changed_files:
    if len(co_changed_files[tup])>=3:
        filtered_sets.append([tup,co_changed_files[tup]])

filtered_sets=sorted(filtered_sets,key=lambda x:-len(x[1]))
filtered_sets = {files: commits for files, commits in filtered_sets}

# Print the filtered sets
filtered_lookup = {"List of Changed Files" : [], "List of Commits" : []}
for files, commits in filtered_sets.items():
    commit_str = ""
    file_str = ""
    for i,commit in enumerate(commits):
        commit_str += f"{i+1}.{commit} "
    for file_name in files:
        file_str+= f"{file_name} "
    filtered_lookup["List of Changed Files"].append("\n".join(file_str.strip().split()))
    filtered_lookup["List of Commits"].append("\n".join(commit_str.strip().split()))

df = pd.DataFrame(filtered_lookup)
df.to_csv(f"{num_files}files.csv",index=False)
