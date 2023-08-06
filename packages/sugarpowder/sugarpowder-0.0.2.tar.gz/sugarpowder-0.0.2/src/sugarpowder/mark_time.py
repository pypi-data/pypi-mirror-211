import time


def mark_time(start_time=None, prompt="", end=False):
    now = time.time()
    if start_time is not None:
        print(f"Elapsed {prompt}: {now-start_time}")
    print(f"Time Marked: {prompt}")
    return now
