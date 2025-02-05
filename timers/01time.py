#通过记录起始时间和结束时间计算执行时间。
import time

# 开始计时
start_time = time.time()

# 模拟某些代码运行
time.sleep(2)

# 结束计时
end_time = time.time()

# 计算耗时
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
