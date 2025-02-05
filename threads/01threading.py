#使用 threading.Thread 创建线程。
import threading
import time

def worker(name):
    print(f"Thread {name} is starting")
    time.sleep(2)
    print(f"Thread {name} is finished")

# 创建线程
thread1 = threading.Thread(target=worker, args=("A",))
thread2 = threading.Thread(target=worker, args=("B",))

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("All threads are done")
