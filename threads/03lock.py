#线程共享全局变量时，可能会导致竞争条件。这时需要使用线程锁。
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    for _ in range(100000):
        with lock:  # 保证线程安全
            counter += 1
            print(counter)

# 创建线程
threads = [threading.Thread(target=increment) for _ in range(5)]

# 启动线程
for t in threads:
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print("Final counter:", counter)
