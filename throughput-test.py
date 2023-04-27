import time
import subprocess
start = time.time()
run_count = 5

def run_code():
    count = 0
    while count < run_count:
        subprocess.call(["python", "main.py"])
        print("---------------------Execution Completed---------------------------------------------")
        count += 1
        print(count)
        print("---------------------Execution Completed---------------------------------------------")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

run_code()
end = time.time()
n = end - start

print('time taken: ')
print(convert(n))
print('hh:mm:ss')