import sys
import time


_time_ticks_ms = time.ticks_ms if hasattr(time, 'ticks_ms') else lambda: time.time_ns() // 1_000_000

if hasattr(sys, "print_exception"):
    def _exception_printer(e: Exception, f):
        sys.print_exception(e, f)
else:
    import traceback
    def _exception_printer(e: Exception, f):
        traceback.print_exception(e, file=f)

class RingBuffer:
    def __init__(self, size=4096, clock=_time_ticks_ms):
        self.size = size
        self.clock = clock
        self.buffer = memoryview(bytearray(size))
        self.pos = 0
    
    def write(self, *args, end="\n"):
        self._write(self.clock())
        self._write(" ")
        for arg in args:
            self._write(arg)
        if end:
            self._write(end)

    def _write(self, arg):
        if isinstance(arg, bytes):
            b = arg
        elif isinstance(arg, str):
            b = arg.encode()
        else:
            b = str(arg).encode()
        
        pos = self.pos
        length = self.size
        end_pos = pos + len(b)
        if end_pos <= length:
            self.buffer[pos:end_pos] = b
            self.pos = end_pos
        else:
            split_pos = length-pos
            new_end_pos = len(b) - split_pos
            self.buffer[pos:length] = b[0:split_pos]
            self.buffer[0:new_end_pos] = b[split_pos:]
            self.pos = new_end_pos
        
        sys.stderr.buffer.write(b)

    def dump_to_file(self, path: str, exc: Exception|None=None):
        with open(path, 'wb') as f:
            f.write(self.buffer[self.pos:])
            f.write(self.buffer[:self.pos])
        if exc:
            with open(path, 'at') as f:
                _exception_printer(exc, f)

LOG = RingBuffer(size=16384)
