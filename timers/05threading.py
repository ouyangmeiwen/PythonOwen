#如果需要定期执行任务，可以结合 threading 和循环实现。
import threading

def periodic_task(interval):
    print("Task executed")
    # 再次启动计时器
    threading.Timer(interval, periodic_task, [interval]).start()

# 每隔 2 秒执行一次任务
periodic_task(2)
print("end")