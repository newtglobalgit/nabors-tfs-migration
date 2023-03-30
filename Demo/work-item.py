import subprocess

p = subprocess.Popen(["powershell.exe", "function Out-Default {}", 
              "C:\\tools\\MigrationTools\\migration.exe execute --config C:\\tools\\MigrationTools\\configuration.json"])
p.communicate()