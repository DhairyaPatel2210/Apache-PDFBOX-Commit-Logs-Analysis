"""
Code analyze all the commits made on the repository by looking for the Issue Id mentioned in the commit message.
NOTE: If the commit message doesn't contain Issue Id, to which commit addresses, then code will not be able to analyze those Issues. 
"""
from pydriller import Repository
import re
import json


"""
this is the lookup which maintain below structure:
{
    "issue_id" : 
                [
                    {
                        "commit_hash":commit.hash,
                        "added_files" : 0,
                        "deleted_files" : 0,
                        "modified_files" : 0  
                    }
                ]
}
"""
lookup = {}

# traversing through all the commits inside the repository
for commit in Repository("https://github.com/apache/pdfbox").traverse_commits():
        
        issues = []  # list of issues the commit addresses
        pattern = r'\bPDFBOX-\d+\b' # regular expression to extract the IssueIds from the commit message
        issues = re.findall(pattern, commit.msg)
        commit_data = {
                "commit_hash":commit.hash,
                "added_files" : 0,
                "deleted_files" : 0,
                "modified_files" : 0  
        }

        # going through all the files that have been modified in commit and depending upon the file change type, updating it's value
        for file in commit.modified_files:
            if file.change_type.name == "ADD":
                commit_data["added_files"]+=1
            if file.change_type.name == "DELETE":
                commit_data["deleted_files"]+=1
            if file.change_type.name == "MODIFY":
                commit_data["modified_files"]+=1
        
        # mapping commit data to all the issues this commit addresses to
        for issue_id in issues:
            if issue_id in lookup:
                lookup[issue_id].append(commit_data)
            else:
                lookup[issue_id] = [commit_data]

# saving the generated data in pr_data.json file
with open("pr_data.json", "w") as outfile: 
    json.dump(lookup, outfile)

            


    

