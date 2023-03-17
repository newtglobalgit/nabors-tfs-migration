from github import Github
from credentials import cred, data

access_token = cred.get('token')
GITHUB_REPO = data.get('name')

g = Github(access_token)

try:
    repo = g.get_user().get_repo(GITHUB_REPO)

except:
    repo = g.get_user().create_repo(GITHUB_REPO)
    repo = g.get_repo(repo)
    repo.create_file("initial.txt", "initialize", "test initialization", branch="master")
print(repo)
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

with open('dummy.txt', 'r') as file:
    content = file.read()

git_prefix = 'tfs1/'
git_file = git_prefix + 'dummy.txt'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, "committing files", content, branch="master")
    print(git_file + ' CREATED')