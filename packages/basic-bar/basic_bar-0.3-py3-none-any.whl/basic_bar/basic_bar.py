import time, sys

def bar(iterable, length=33):
    total, start = len(iterable), time.monotonic()
    for count, it in enumerate(iterable, 1):
        yield it
        elapsed_time, remaining_time = time.monotonic() - start, (time.monotonic() - start) / count * (total - count)
        percent, filled_len = count / total, int(length * (count / total))
        sys.stdout.write(f'\r▕{"█" * filled_len}{" " * (length - filled_len)}▏ {percent*100:.2f}% {remaining_time:.2f}s'), sys.stdout.flush()
    sys.stdout.write(f'\r▕{"█" * length}▏ 100.00% {time.monotonic() - start:.2f}s\n')
