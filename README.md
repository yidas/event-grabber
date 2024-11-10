# Grabbing Tool

Python grabbing tool

---

## Usage

Quick Install:

```shell
$ git clone https://github.com/yidas/event-grabber.git
```

Set the command content for the target event and the log file path, then run it on event time:

```shell
$ python3 event-grabber/grabbing.py -c "bash grabber.sh" -f "grabber.log"
```

In addition, you can set a fixed time to execute:

```shell
$ python3 event-grabber/grabbing.py -t 23:59:59
```

For the session timeout issue, maybe it's better to periodically to trigger the target execution one-time before actual execution (Unit: second):

```shell
$ python3 event-grabber/grabbing.py -t 23:59:59 -r 1800
```

For automation, use `nohup` with `&` symbol to execute in the background


```shell
$ nohup python3 event-grabber/grabbing.py -t 23:59:59 &
```

---

## Options

```
$ python3 grabbing.py --help
options:
  -h, --help            show this help message and exit
  -t [N], --time [N]    Execution target time for timer
  -r [N], --renew-seconds [N]
                        Execute once per frequency during timer running
  -e [N], --early-seconds [N]
                        The seconds to execute ahead for timer (Should be < 1.0)
  -d [N], --duration-seconds [N]
                        The duration seconds for execution
  -i [N], --interval-seconds [N]
                        The interval seconds to execute in duration
  -c [N], --cmd [N]     Execution command line
  -f [N], --log-file [N]
                        Log file for each execution
  -l [N], --loop-times [N]
                        Execution loop times
```
