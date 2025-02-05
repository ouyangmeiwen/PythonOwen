#守护线程会在主线程结束时自动退出。
import threading
import time

def background_task():
    while True:
        print("Running in the background...")
        time.sleep(1)

# 创建守护线程
daemon_thread = threading.Thread(target=background_task, daemon=True)
daemon_thread.start()

# 主线程运行 3 秒后结束
time.sleep(3)
print("Main thread is exiting")
