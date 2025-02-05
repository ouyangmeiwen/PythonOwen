#threading.Timer 可用来在指定的时间后执行某个函数。
import threading

def say_hello():
    print("Hello, this is a timed message!")

# 创建一个 5 秒的计时器
timer = threading.Timer(5.0, say_hello)

# 启动计时器
timer.start()

print("Timer started, waiting for 5 seconds...")
