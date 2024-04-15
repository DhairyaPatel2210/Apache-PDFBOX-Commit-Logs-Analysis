"""
Code generates the CSV file as per the instructions of the assignment using pr_data.json file
"""

import json
import pandas as pd

# Opening JSON file
f = open('pr_data.json')
 
# loading the issue data in the issue_data 
issue_data = json.load(f)

# this structured data is being used to generate CSV file using Pandas
structured_data = {"ISSUE_ID":[],"Commits":[],"Added":[], "Modified":[],"Deleted":[]}

# iterating through each issue in the issue_data and structuring it properly
for issue in issue_data.keys():
    added = 0
    modified = 0
    deleted = 0
    commits_list = []
    commits = issue_data[issue]
    for c in commits:
        commits_list.append(c["commit_hash"])
        modified+=c["modified_files"]
        deleted+=c["deleted_files"]
        added+=c["added_files"]
    structured_data["ISSUE_ID"].append(issue)
    structured_data["Commits"].append(commits_list)
    structured_data["Added"].append(added)
    structured_data["Modified"].append(modified)
    structured_data["Deleted"].append(deleted)

# creating DataFrame from the structured_data using Pandas
df = pd.DataFrame(structured_data)

# converting CSV file from the pandas DataFrame
df.to_csv("analyzed_issue.csv",index=False)