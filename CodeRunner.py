import time
import Migration as migration

class CodeRunner:
    def __init__(self, run_count):
        self.run_count = run_count

    def run_code(self):
        count = 0
        while count < self.run_count:
            print("---------------------Execution Started-----------------------------------------------")
            migration.run()
            count += 1
            print(count)
            print("---------------------Execution Completed---------------------------------------------")

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

if __name__ == '__main__':
    start = time.time()
    run_count = 1
    code_runner = CodeRunner(run_count)
    code_runner.run_code()
    end = time.time()
    n = end - start
    print('time taken: ')
    print(code_runner.convert(n))
    print('hh:mm:ss')