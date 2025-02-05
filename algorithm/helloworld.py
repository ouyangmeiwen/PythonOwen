import ctypes

# 加载共享库
lib = ctypes.CDLL('./algorithm/libInvengo.Library.Algorithm.so')  # 对于 Windows 使用 mylibrary.dll

# 调用 C++ 函数
lib.hello_from_cpp()