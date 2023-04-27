from github import Github
import pandas as pd
from credentials import cred

token = cred.get('token')
owner = cred.get('owner')

def get_file_structure_to_excel(access_token, repo_name, branch_name,user_name):
    g = Github(access_token)
    repo = g.get_repo(f'{user_name}/{repo_name}')
    file_structure = pd.DataFrame(columns=['Directory', 'File_Name', 'File_Type', 'Size(Byte)'])
    contents = repo.get_contents("", ref=branch_name)
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            if file_content.name == ".git":
                continue
            contents.extend(repo.get_contents(file_content.path, ref=branch_name))
        else:
            if file_content.name in [".gitattributes", ".git"]:
                continue
            extension = file_content.name.split(".")[-1] if "." in file_content.name else ""
            directory = "/".join(file_content.path.split("/")[:-1])
            if not directory:
                directory_path = branch_name
            else:
                directory_path = branch_name+"/"+directory
            file_structure = file_structure.append({
                'Directory': directory_path,
                'File_Name': file_content.name,
                'File_Type': "."+extension,
                'Size(Byte)': file_content.size
            }, ignore_index=True)

    file_structure.to_excel("file_structure_{}.xlsx".format(branch_name), index=False)


get_file_structure_to_excel(token, "CatCore", "cleanup",owner)