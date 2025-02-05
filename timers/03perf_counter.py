#time.perf_counter 提供了更高精度的计时，非常适合精确测量小时间间隔。
import time

# 开始计时
start = time.perf_counter()

# 模拟运行一些代码
time.sleep(1)

# 结束计时
end = time.perf_counter()

print(f"Elapsed time: {end - start:.6f} seconds")
