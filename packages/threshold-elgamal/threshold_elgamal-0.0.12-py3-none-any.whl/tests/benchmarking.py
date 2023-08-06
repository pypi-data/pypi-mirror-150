import time

from threshold_elgamal import *


def time_func(func, *args, **kwargs):
    runtimes = 0
    for _ in range(3):
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        runtime = end_time - start_time
        runtimes += runtime
    avg_runtime_ = runtimes / 3
    return avg_runtime_


for length in [2048, 3072, 4096]:
    for n in [1, 3, 5, 10, 20]:
        for k in [1, int(n/2), n-1]:
            try:
                avg_runtime = time_func(run_tc_scheme, k, n, 10, length)
                print(length, n, k, avg_runtime, sep=" & ")
            except BaseException:
                continue

