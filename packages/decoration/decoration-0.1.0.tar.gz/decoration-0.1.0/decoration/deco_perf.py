import functools
import time

disrupt = True


def run_time(func):
    @functools.wraps(func)
    def run_time_wrapper(*args, **kwargs):
        if disrupt:
            print(f"----Measure run_time func name: {func.__name__}")
            start_time = time.perf_counter()
            func_ret = func(*args, **kwargs)
            # time.sleep(1)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            # print("Do something after func call !!")
            print(f"args: {args}")
            print(f"kwargs: {kwargs}")
            print(f"duration [msecs]: {(run_time*1000):.6f}")
            print(f"return value: {func_ret}")
        else:
            func_ret = func(*args, **kwargs)
        return func_ret

    return run_time_wrapper
