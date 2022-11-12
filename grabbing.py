# Config
intervalSeconds = 0.1
durationSeconds = 10
cmd = "bash grabbing.sh"
logFile = "grabbing.log"
resetLog = True

# Main
import os
import time
import multiprocessing as mp

def work(num):
    output = os.popen(cmd).read()
    log = "\r\nLog by process {}: \r\n".format(num) + output.strip() + "\r\n"
    f = open(logFile, "a")
    f.write(log)
    f.close()

# Main process
if __name__ == '__main__':
    processNum = int(round(durationSeconds / intervalSeconds))

    if resetLog:
        f = open(logFile, "w")
        # f.write(str(output))
        f.close()

    # print(processNum)
    process = {}
    for i in range(processNum):
        process[i] = mp.Process(target=work, args = (i,))
        process[i].start()
        time.sleep(intervalSeconds)

