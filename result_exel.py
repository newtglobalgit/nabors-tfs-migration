import openpyxl
import winrm
from credentials import cred, server, path

# Create a new workbook and sheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# Add header row to the sheet
sheet['A1'] = 'Directory Name'
sheet['B1'] = 'Type'

# Loop through each directory
row_num = 2 # start from row 2 since row 1 is the header
cd1 = sess.run_ps("Set-Location "+defpath)
result = sess.run_ps("Get-ChildItem -Directory "+defpath +"| select Name")
directories = result.std_out.splitlines()
for directory in directories[3:]:
    if len(directory) >0:
        dir_path = directory.decode('utf-8')
        print(dir_path)
        print("------------")
        child_dir=defpath+dir_path
        cd2 = sess.run_ps("Set-Location "+defpath+dir_path)
        result2 = sess.run_ps("Get-ChildItem "+defpath+dir_path+"| Select-Object Name,PSIsContainer")
            # Get-ChildItem -Path <path_to_directory> -Recurse | Select-Object Name, IsBinary
            
        directories2 = result2.std_out.splitlines()
            
        if len(directory) >0:
            for directory1 in directories2[3:]:
                    
                if len(directory1) >0:
                    dir_name = directory1.decode('utf-8')
                    
                    if "True" in dir_name:
                        dir_name_new = dir_name.split("True")
                        print("dir ",dir_name_new[0] )
                    else :
                        dir_name_new = dir_name.split("False")
                        print("file",dir_name_new[0] )
            print()
# Save the workbook
workbook.save('output.xlsx')
