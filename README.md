# Grabbing Tool

Python grabbing tool

---

## Usage

Quick Install:

```shell
$ git clone https://github.com/yidas/event-grabber.git
```

Set the command content for the target event, and then run it on event time:

```shell
$ python3 
```

In addition, you can set a fixed time to execute:

```shell
$ python3 event-grabber/grabbing.py 23:59:59
```

For the session timeout issue, maybe it's better to periodically to trigger the target execution one-time before actual execution (Unit: second):

```shell
$ python3 event-grabber/grabbing.py 23:59:59 1800
```

For automation, use `nohup` with `&` symbol to execute in the background


```shell
$ nohup python3 event-grabber/grabbing.py 23:59:59 &
```
