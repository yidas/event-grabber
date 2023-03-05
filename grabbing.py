# Config
intervalSeconds = 0.15
durationSeconds = 0.45
timerEarlySeconds = 0.2  # Shoud < 1.0 
cmd = "bash grabbing.sh"
logFile = "grabbing.log"
resetLog = True

# Main
import sys
import os
import time
import threading
from datetime import datetime, timedelta

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

def countDownTimer(timeString: str, renewCount: int = 0):
    # print(timeString + " renew:" + renewCount)
    renewCount = int(renewCount)
    targetTimeList = timeString.split(':')
    # print(targetTimeList)

    # Target time setting
    targetTime = datetime.now()
    targetTime = targetTime.replace(microsecond=0)
    if len(targetTimeList) > 0:
        targetTime = targetTime.replace(hour=int(targetTimeList[0]))
    targetTime = targetTime.replace(minute=int(targetTimeList[1])) if len(targetTimeList) > 1 else targetTime.replace(minute=0)
    targetTime = targetTime.replace(second=int(targetTimeList[2])) if len(targetTimeList) > 2 else targetTime.replace(second=0)
    # Diff input
    targetTime =  targetTime - timedelta(seconds=1)
    # print(targetTime)

    # Panel display
    currentTime = datetime.now()
    # Check if is in tomorrow
    if currentTime > targetTime:
        targetTime = targetTime + timedelta(days=1)
    timeDiff = targetTime - currentTime
    hours, remainder = divmod(timeDiff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    timeDiffString = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    print("Current Time: {} \r\nExecution Time: {} \r\nRemaining seconds: {}".format(currentTime.strftime("%Y-%m-%d %H:%M:%S"), targetTime, timeDiffString))

    # Loop checker
    count = 0
    while True:
        # Diff time
        timeDiff = targetTime - currentTime
        diffSeconds = timeDiff.seconds
        # About to start
        if diffSeconds < 10 and diffSeconds > 0:
            if count > 9:
                print("Countdown second: {}".format(diffSeconds))
                count = 0
            # Short sleep
            time.sleep(0.1)
        else:
            # Sleep
            time.sleep(1)
            if renewCount > 0 and count >= renewCount:
                output = os.popen(cmd).read()
                count = 0
        # Update current timer   
        # Renew
        count += 1     
        currentTime = datetime.now()
        # Exit statement
        if targetTime < currentTime:
            break
    diffTotalSeconds = timeDiff.total_seconds()
    # Fulfill sleep to align start second timerEarlySeconds
    time.sleep(max(0, diffTotalSeconds - float(timerEarlySeconds)))

# Main process
if __name__ == '__main__':

    # Countdown timer
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            countDownTimer(sys.argv[1], sys.argv[2])
        else:
            countDownTimer(sys.argv[1])
        
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
