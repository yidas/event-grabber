# Config
intervalSeconds = 0.5
durationSeconds = 5
cmd = "bash grabbing.sh"
logFile = "grabbing.log"
resetLog = True

# Main
import sys
import os
import time
import threading
from datetime import datetime

def work(num):
    timeStart = datetime.now()
    # Execute command
    output = os.popen(cmd).read()
    timeEnd = datetime.now()
    timeDiff = timeEnd - timeStart
    log = "\r\nLog by process {} ({} - {} | Total: {}s): \r\n".format(num, timeStart.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], timeEnd.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], timeDiff.total_seconds()) + output.strip() + "\r\n"
    # Write to log
    f = open(logFile, "a")
    f.write(log)
    f.close()

# Main process
if __name__ == '__main__':

    # Countdown timer
    if len(sys.argv) > 1:
        argv1 = sys.argv[1]
        # print(argv1)
        targetTimeList = argv1.split(':')
        # print(targetTimeList)

        # Target time setting
        targetTime = datetime.now()
        targetTime = targetTime.replace(microsecond=0)
        if len(targetTimeList) > 0:
            targetTime = targetTime.replace(hour=int(targetTimeList[0]))
        if len(targetTimeList) > 1:
            targetTime = targetTime.replace(minute=int(targetTimeList[1]))
        if len(targetTimeList) > 2:
            targetTime = targetTime.replace(second=int(targetTimeList[2]))
        # print(targetTime)

        currentTime = datetime.now()
        print("Current Time: {}\r\nExecution Time: {}".format(currentTime.strftime("%Y-%m-%d %H:%M:%S"), targetTime))

        # Loop checker
        while targetTime > currentTime:
            # Diff time
            timeDiff = targetTime - currentTime
            diffSecond = timeDiff.seconds
            if diffSecond < 10 and diffSecond > 0:
                print("Countdown second: {}".format(diffSecond))
            # Sleep
            time.sleep(1)
            currentTime = datetime.now()

    # Execution
    print("Begin execution...")
    processNum = int(round(durationSeconds / intervalSeconds))

    if resetLog:
        f = open(logFile, "w")
        # f.write(str(output))
        f.close()

    # print(processNum)
    threads = {}
    for i in range(processNum):
        threads[i] = threading.Thread(target=work, args = (i,))
        threads[i].start()
        time.sleep(intervalSeconds)

    # Wait for all workers to complete
    for i in threads:
        threads[i].join()

    print("\r\nDone. logFile: {}".format(logFile))
