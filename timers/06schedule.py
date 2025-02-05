## 安装 schedule 库
#pip install schedule
import schedule
import time

def job():
    print("Task executed!")

# 每隔 5 秒执行一次
schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)  # 防止高频空循环
    
print("end")