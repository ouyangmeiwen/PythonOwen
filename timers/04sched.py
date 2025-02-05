#sched 模块可以用来安排任务在指定时间点执行
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def scheduled_task():
    print("Task executed at:", time.time())

# 安排任务在 3 秒后执行
scheduler.enter(3, 1, scheduled_task)
print("Task scheduled, waiting...")

# 开始调度
scheduler.run()
print("end")
