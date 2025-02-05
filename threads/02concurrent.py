#使用 concurrent.futures.ThreadPoolExecutor 可以更方便地管理线程池。
from concurrent.futures import ThreadPoolExecutor
import time

def worker(name):
    print(f"Thread {name} is starting")
    time.sleep(2)
    print(f"Thread {name} is finished")

# 创建线程池
with ThreadPoolExecutor(max_workers=3) as executor:
    for i in range(5):
        executor.submit(worker, f"Worker-{i}")
