from lib.logging import RingBuffer


def test_ringbuffer_write_and_wrap():
    rb = RingBuffer(size=12, clock=lambda: 999)
    
    rb.write("12345")
    assert bytes(rb.buffer) == b"999 12345\n\x00\x00"

    rb.write("67890")
    assert bytes(rb.buffer) == b"9 67890\n5\n99"

    # Buffer should wrap around after 10 bytes
    rb.write("abc")
    assert bytes(rb.buffer) == b"abc\n890\n999 "

def test_ringbuffer_write_bytes_and_str():
    rb = RingBuffer(size=11, clock=lambda: 0)
    
    rb.write(b"hi", "there")
    assert bytes(rb.buffer) == b"0 hithere\n\x00"

def test_ringbuffer_write_numbers():
    rb = RingBuffer(size=11, clock=lambda: 0)
    
    rb.write(123, 45.6)
    assert bytes(rb.buffer) == b"0 12345.6\n\x00"

def test_ringbuffer_dump_to_file(tmp_path):
    rb = RingBuffer(size=12, clock=lambda: 0)

    rb.write("123456789", "abcdefghi")
    file_path = tmp_path / "ringbuffer_dump.bin"
    rb.dump_to_file(str(file_path))

    with open(file_path, "rb") as f:
        data = f.read()
    assert data == b"89abcdefghi\n"

def test_ringbuffer_dump_with_traceback(tmp_path):
    rb = RingBuffer(size=1024)
    file_path = tmp_path / "ringbuffer_dump.bin"

    def failing_method(a: int):
        _ = a / 0

    try:
        failing_method(1)
    except Exception as e:
        rb.dump_to_file(file_path, e)
        with open(file_path, "rb") as f:
            data = f.read()

    # Check that part of the traceback is in the buffer
    assert b"test_ringbuffer_dump_with_traceback" in data
    assert b"failing_method" in data
    assert b"ZeroDivisionError" in data
