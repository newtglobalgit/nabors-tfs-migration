import subprocess

folder_path = r"C:\Demo\dprog"
cmd = 'Remove-Item -Path "{folder_path}" -Recurse -Force'
result = subprocess.run(cmd)
print()