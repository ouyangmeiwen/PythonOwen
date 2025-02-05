
from collections import Counter

if __name__ == "__main__":
    ###判定data1中的那么是否有重复的
    data1 = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 32},
        {'name': 'Bob', 'age': 32},
        {'name': 'Bob', 'age': 32},
        {'name': 'Charlie', 'age': 28}
    ]


    #使用集合（set）
    # 提取所有name组成一个集合
    names = set(item['name'] for item in data1)
    # 判断集合长度和原始列表长度是否相等
    if len(names) == len(data1):
        print("没有重复的name")
    else:
        print("有重复的name")


    #使用字典
    name_counts = {}
    for item in data1:
        name = item['name']
        name_counts[name] = name_counts.get(name, 0) + 1
    has_duplicates = any(count > 1 for count in name_counts.values())
    print(has_duplicates)

    #使用Counter
    names = [item['name'] for item in data1]
    name_counts = Counter(names)
    has_duplicates = any(count > 1 for count in name_counts.values())
    print(has_duplicates)

