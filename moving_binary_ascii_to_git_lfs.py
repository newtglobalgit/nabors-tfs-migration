import os
import winrm
from credentials import cred, server, path


user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')

sess = winrm.Session(url, auth=(user, password), transport='ntlm')

def moving_binary_ascii_to_git_lfs(defpath):
    
    ASCII_EXTENSIONS = ['.txt', '.py', '.c', '.cpp', '.h', '.hpp', '.md', '.html', '.css', '.js','.jpg', '.jpeg', '.png', '.gif', '.mp4', '.pdf', '.doc', '.xls', '.ppt','.exe','.dll','.bin']

    # ps_cmd = "powershell.exe"
    ps_cmd = f'Set-Location "{defpath}"'
    # ps_cmd1 = f'New-Variable -Name defpath -Value "{defpath}"'
    ps_cmd2 = 'Get-ChildItem -Path $defpath | Where-Object { !$_.PSIsContainer } | ForEach-Object {'
    ps_cmd3 = '$filename = $_.Name'
    ps_cmd4 = '$file_ext = [System.IO.Path]::GetExtension($filename).ToLower()'
    ps_cmd5 = 'if ($file_ext -in ${ASCII_EXTENSIONS}) {'
    ps_cmd6 = '$cmd9 = "git lfs migrate import --include=`"$filename`""'
    ps_cmd7 = '$cmd10 = "git add ."'
    ps_cmd8 = '$cmd11 = "git commit -m `"`"Moving $filename to Git LFS`"`""'
    ps_cmd9 = '& cmd.exe /c $cmd9'
    ps_cmd10 = '& cmd.exe /c $cmd10'
    ps_cmd11 = '& cmd.exe /c $cmd11'
    ps_cmd12 = '}'
    ps_cmd13 = '}'
    ps_cmd14 = '& cmd.exe /c "git push"'
    
    ps_commands = [ps_cmd2, ps_cmd3, ps_cmd4, ps_cmd5, ps_cmd6, ps_cmd7, ps_cmd8, ps_cmd9, ps_cmd10, ps_cmd11, ps_cmd12, ps_cmd13, ps_cmd14]
    
    full_ps_cmd = "; ".join(ps_commands)
    output =sess.run_ps(ps_cmd + ';' + full_ps_cmd)
    print(output)


