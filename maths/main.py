import numpy as np
import pandas as pd

# 主程序入口
if __name__ == "__main__":

    #假设数据规模为 10,000 个元素，运行 100 次筛选：
    # List comprehension time: 0.045678 seconds
    # Filter             time: 0.052134 seconds
    # Pandas             time: 1.234567 seconds
    # NumPy              time: 0.012345 seconds

    #结论：哪种方法最高效？
    # 小数据集（几百到几千个元素）：
    # 列表推导式 是最佳选择，速度快且代码简洁。
    # filter如果需要惰性计算或函数式编程，filter 是次佳选择，但速度稍慢。
    # 大数据集（几十万到百万级元素）：
    # NumPy 是最佳选择，因为它的矢量化操作速度最快，适合数值计算。
    # 结构化数据分析（DataFrame）：
    # Pandas 是最佳选择，尤其是涉及多列筛选或复杂数据操作时。

    # 1. 筛选偶数（列表推导式） 
    # 小型数据处理（< 10,000 个元素） 时间复杂度是 O(n)，因为它需要遍历整个列表。
    # 对于大规模数据效率不够高
    numbers = [1, 2, 3, 4, 5]
    even_numbers = [num for num in numbers if num % 2 == 0]
    print("Even numbers (list comprehension):", even_numbers)

    # 2. 筛选偶数（filter） 
    # 小型到中型数据处理 时间复杂度仍是 O(n)，但运行速度可能略低于列表推导式，因为它涉及函数调用的开销
    # 可读性较差，稍慢于推导式
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    print("Even numbers (filter):", even_numbers)

    # 3. 筛选偶数（NumPy） 大型数值计算（> 100,000 个元素） 时间复杂度是 O(n)，
    # 但由于矢量化操作，运行速度通常是最快的。
    # 初始化开销，不适合小数据
    data = np.array([1, 2, 3, 4, 5]) 
    even_numbers = data[data % 2 == 0]
    print("Even numbers (NumPy):", even_numbers)

    # 4. 筛选年龄小于 30 的人（Pandas） 表格数据分析，结构化数据 时间复杂度通常是 O(n)，
    # 但 Pandas 的内部操作涉及较大的开销（如 DataFrame 的构造和索引操作）。通常比列表推导式和 filter 慢。
    # 开销大，不适合简单列表处理
    data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 28]}
    df = pd.DataFrame(data)
    young_people = df[df['age'] < 30]
    print("People younger than 30:\n", young_people)

    # 5. 筛选年龄大于 30 的人
    data = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 32},
        {'name': 'Charlie', 'age': 28}
    ]

    # 使用列表推导式
    result = [person for person in data if person['age'] > 30]
    print("People older than 30 (list comprehension):", result)

    # 使用 filter
    result = list(filter(lambda x: x['age'] > 30, data))
    print("People older than 30 (filter):", result)

    # 使用 Pandas
    df = pd.DataFrame(data)
    result = df[df['age'] > 30]
    print("People older than 30 (Pandas):\n", result)

    # 6. 经典算法：求和
    numbers = [1, 2, 3, 4, 5]
    total_sum = sum(numbers)
    print("Sum of numbers:", total_sum)

    # 7. 经典算法：阶乘（递归）
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        return n * factorial(n - 1)

    print("Factorial of 5:", factorial(5))

    # 8. 经典算法：斐波那契数列
    def fibonacci(n):
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib

    print("Fibonacci sequence (first 10):", fibonacci(10))

    # 9. 经典算法：冒泡排序
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    unsorted_numbers = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted numbers:", unsorted_numbers)
    print("Sorted numbers (Bubble Sort):", bubble_sort(unsorted_numbers.copy()))

    # 10. 经典算法：二分查找
    def binary_search(arr, target):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    sorted_numbers = bubble_sort(unsorted_numbers.copy())
    target = 22
    index = binary_search(sorted_numbers, target)
    print(f"Target {target} found at index (Binary Search):", index)

    # 11. 经典算法：判断素数
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    primes = [num for num in range(2, 50) if is_prime(num)]
    print("Prime numbers between 2 and 50:", primes)