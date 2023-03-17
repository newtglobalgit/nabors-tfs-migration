import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.3.197', username='ujjawal', password='Trade@1234')

stdin, stdout, stderr = ssh.exec_command('ls -l')

for line in stdout:
    print(line.strip())

ssh.close()