# Config
config = {
    'intervalSeconds': 0.3,
    'durationSeconds': 0.3,
    'timerEarlySeconds': 0.3,
    'cmd': "bash grabbing.sh",
    'logFile': "grabbing.log",
    'time': None,
    'renewSeconds': 0,
    'loopTimes': 0,
    'resetLog': True
}

# Main
import sys
import os
import time
import threading
from datetime import datetime, timedelta
import argparse

# Main process
def main(config: dict):

    # Countdown timer
    if (config['time']):
        countDownTimer(config, config['time'], config['renewSeconds'])
    
    # Execution
    print("Begin execution...")
    processNum = int(round(config['durationSeconds'] / config['intervalSeconds']) + 1)

    # print(processNum)
    threads = {}
    for i in range(processNum):
        threads[i] = threading.Thread(target=work, args = (i, config,))
        threads[i].start()
        time.sleep(config['intervalSeconds'])

    # Wait for all workers to complete
    for i in threads:
        threads[i].join()

# Thread
def work(num, config: dict):

    timeStart = datetime.now()
    # Execute command
    output = os.popen(config['cmd']).read()
    timeEnd = datetime.now()
    timeDiff = timeEnd - timeStart
    log = "\r\nLog by process {} ({} - {} | Total: {}s): \r\n".format(num, timeStart.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], timeEnd.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], timeDiff.total_seconds()) + output.strip() + "\r\n"
    # Write to log
    f = open(config['logFile'], "a")
    f.write(log)
    f.close()

# Countdown timer
def countDownTimer(config: dict, timeString: str, renewCount: int = 0):
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
                output = os.popen(config['cmd']).read()
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
    time.sleep(max(0, diffTotalSeconds - float(config['timerEarlySeconds'])))

# Main process
if __name__ == '__main__':
        
    # ArgumentParser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', '--time', metavar='N', type=str, nargs='?', default=None,
                        help='Execution target time for timer')
    parser.add_argument('-r', '--renew-seconds', metavar='N', type=int, nargs='?', default=None,
                        help='Execute once per frequency during timer running')
    parser.add_argument('-e', '--early-seconds', metavar='N', type=float, nargs='?', default=None,
                        help='The seconds to execute ahead for timer (Shoud < 1.0)')
    parser.add_argument('-d', '--duration-seconds', metavar='N', type=float, nargs='?', default=None,
                        help='The duration seconds for execution')
    parser.add_argument('-i', '--interval-seconds', metavar='N', type=float, nargs='?', default=None,
                        help='The interval seconds to execute in duration')
    parser.add_argument('-c', '--cmd', metavar='N', type=str, nargs='?', default=None,
                        help='Execution command line')
    parser.add_argument('-f', '--log-file', metavar='N', type=str, nargs='?', default=None,
                        help='Log file for each execution')
    parser.add_argument('-l', '--loop-times', metavar='N', type=int, nargs='?', default=None,
                        help='Execution loop times')
    args, unknown_args = parser.parse_known_args()
    print('Args:', args);

    # Parameter override
    config['durationSeconds'] = args.duration_seconds if args.duration_seconds is not None else config['durationSeconds']
    config['intervalSeconds'] = args.interval_seconds if args.interval_seconds else config['intervalSeconds']
    config['time'] = args.time if args.time else config['time']
    config['timerEarlySeconds'] = args.early_seconds if args.early_seconds else config['timerEarlySeconds']
    config['renewSeconds'] = args.renew_seconds if args.renew_seconds else config['renewSeconds']
    config['cmd'] = args.cmd if args.cmd else config['cmd']
    config['logFile'] = args.log_file if args.log_file else config['logFile']
    config['loopTimes'] = args.loop_times if args.loop_times else config['loopTimes']
    print('Config:', args);

    # Log clearing function
    if config['resetLog']:
        f = open(config['logFile'], "w")
        # f.write(str(output))
        f.close()

    for i in range(config['loopTimes']+1):
        main(config)

    print("\r\nDone. logFile: {}".format(config['logFile']))
