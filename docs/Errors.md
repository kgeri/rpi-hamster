# Errors and their causes

## Freezes

Likely an OOME, but can sometimes be bus errors/timeouts as well - see below.

## QMI8658 errors

Apparently, the `QMI8658` module (or power, or the bus, or a zillion other things) is flaky.
Catching these errors and ignoring them for now.

```txt
Traceback (most recent call last):
  File "main.py", line 39, in <module>
  File "./src/hamster.py", line 19, in tick
  File "./src/hamster.py", line 36, in _simulate
  File "./src/lib/waveshare.py", line 379, in read_axyz_gxyz
  File "./src/lib/waveshare.py", line 417, in _read_raw_xyz
  File "./src/lib/waveshare.py", line 407, in _read_block
OSError: [Errno 110] ETIMEDOUT
```

```txt
Traceback (most recent call last):
  File "main.py", line 36, in <module>
  File "./src/hamster.py", line 19, in tick
  File "./src/hamster.py", line 36, in _simulate
  File "./src/lib/waveshare.py", line 379, in read_axyz_gxyz
  File "./src/lib/waveshare.py", line 417, in _read_raw_xyz
  File "./src/lib/waveshare.py", line 407, in _read_block
OSError: [Errno 5] EIO
```
