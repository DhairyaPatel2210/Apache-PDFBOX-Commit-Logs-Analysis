"""
Code Mine all the files changed for the particular commit
"""

from pydriller import Repository
import json

"""
code to store the structured data as below:
{
    "commit_hash1" : ["f1", "f2", "f4"],
    "commit_hash2" : ["f3", "f6", "f5"]
}
"""
lookup = {}

# iterating through all the commits in the repository
for commit in Repository("https://github.com/apache/pdfbox").traverse_commits():
    for file in commit.modified_files:
        if file.change_type.name == "DELETE":
            if commit.hash in lookup:
                lookup[commit.hash].append(file.old_path)
            else:
                lookup[commit.hash] = [file.old_path]
        else:
            if commit.hash in lookup:
                lookup[commit.hash].append(file.new_path)
            else:
                lookup[commit.hash] = [file.new_path]

# storing the structured data to commit_data.json file
with open("commit_data.json", "w") as outfile: 
    json.dump(lookup, outfile)