import ctypes
import random
import time

# 假设 `lib` 是加载的 C++ 库，且已包含 `AnalyzeTagsString` 函数
lib = ctypes.CDLL('./test/algorithm/libInvengo.Library.Algorithm.so')  # 对于 Windows 使用 mylibrary.dll

# 声明 AnalyzeTagsString 函数原型
lib.AnalyzeTagsString.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
lib.AnalyzeTagsString.restype = ctypes.c_char_p

def analyze_tags(tags_string, min_rssi, max_rssi):
    # 将输入的标签字符串转换为字节格式 (C 风格的字符串)
    tags_string_bytes = tags_string.encode('utf-8')

    # 调用 C++ 的 AnalyzeTagsString 函数
    result_cstr = lib.AnalyzeTagsString(tags_string_bytes, min_rssi, max_rssi)
    
    # 将返回的 C 字符串转换为 Python 字符串
    result_str = ctypes.cast(result_cstr, ctypes.c_char_p).value.decode('utf-8')
    
    # 打印返回的结果，每个标签字段按“#”分隔
    tags = result_str.split('#')
    for tag in tags:
        if tag:
            fields = tag.split('_')
            print(f"EPC: {fields[0]}, RSSI: {fields[1]}, ReadCount: {fields[2]}, Antenna: {fields[3]}")
    
# 示例调用
def generate_tags(num_tags):
    tags = []
    i=0
    for _ in range(num_tags):
        epc = f"远望谷EPC{random.randint(1000, 1050)}"  # 随机生成 EPC 编号

        rssi = round(random.uniform(-80.0, -30.0), 1)  # 随机生成 RSSI 值 (-80 到 -30 之间)
        read_count = random.randint(1, 50)  # 随机生成 ReadCount (1 到 50 之间)
        antenna = random.randint(1, 5)  # 随机生成天线编号 (1 到 3 之间)
        tag = f"{epc}_{rssi}_{read_count}_{antenna}_测试"
        tags.append(tag)
        i=i+1
        print(f"{i}:{epc}:{rssi}")
    return '#'.join(tags)  # 使用 # 将标签拼接成一个大的字符串
# 记录开始时间
start_time = time.time()
print("开始生成标签")
# 生成 100 个标签
tags = generate_tags(1000)
print("结束生成标签")

# 记录结束时间
end_time = time.time()

# 打印执行时间
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


min_rssi = -59.0
max_rssi = 999

analyze_tags(tags, min_rssi, max_rssi)
