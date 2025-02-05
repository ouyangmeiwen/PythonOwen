#如果需要记录函数运行时间，可以使用装饰器。
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@timer
def example_task():
    time.sleep(2)
    print("Task complete!")

example_task()
