# Config
intervalSeconds = 0.15
durationSeconds = 0.45
timerEarlySeconds = 0.3
cmd = "bash grabbing.sh"
logFile = "grabbing.log"
resetLog = True

# Main
import sys
import os
import time
import threading
from datetime import datetime, timedelta
import argparse

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

def countDownTimer(timeString: str, renewCount: int = 0, timerEarlySeconds = timerEarlySeconds):
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
        
    # ArgumentParser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', '--time', metavar='N', type=str, nargs='?', default=None,
                        help='Execution target time for timer')
    parser.add_argument('-r', '--renew-seconds', metavar='N', type=int, nargs='?', default=0,
                        help='Execute once per frequency during timer running')
    parser.add_argument('-e', '--early-seconds', metavar='N', type=float, nargs='?', default=None,
                        help='The seconds to execute ahead for timer (Shoud < 1.0)')
    parser.add_argument('-d', '--duration-seconds', metavar='N', type=float, nargs='?', default=None,
                        help='The duration seconds for execution')
    parser.add_argument('-i', '--interval-seconds', metavar='N', type=float, nargs='?', default=None,
                        help='The interval seconds to execute in duration')
    parser.add_argument('-c', '--cmd', metavar='N', type=str, nargs='?', default=None,
                        help='Execution command line')
    parser.add_argument('-l', '--log-file', metavar='N', type=str, nargs='?', default=None,
                        help='Log file for each execution')
    args, unknown_args = parser.parse_known_args()
    print('Args:', args);

    # Countdown timer
    if (args.time):
        countDownTimer(args.time, args.renew_seconds)

    # Parameter initialization
    durationSeconds = args.duration_seconds if args.duration_seconds else durationSeconds
    intervalSeconds = args.interval_seconds if args.interval_seconds else intervalSeconds
    cmd = args.cmd if args.cmd else cmd
    logFile = args.log_file if args.log_file else logFile
    
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
