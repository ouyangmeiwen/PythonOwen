if __name__ == "__main__":
    ###获取在data1种不在data2中的元素
    data1 = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 32},
        {'name': 'Charlie', 'age': 28}
    ]

    data2 = [
        {'name': 'Alice1', 'age': 25},
        {'name': 'Bob1', 'age': 32},
        {'name': 'Charlie', 'age': 28}
    ]

    #方法一：使用集合 (set) 进行比较
    # 提取 data1 中的 name
    names_in_data1 = set(item['name'] for item in data1)
    # 提取 data2 中的 name
    names_in_data2 = set(item['name'] for item in data2)
    # 求差集，得到 data1 中不在 data2 中的 name
    different_names = names_in_data1 - names_in_data2
    print(different_names)  # 输出: {'Alice', 'Bob'}


    #方法二：使用循环和字典
    # 创建一个字典，以 data2 中的 name 为键
    name_dict = {item['name']: True for item in data2}
    different_names = []
    for item in data1:
        if item['name'] not in name_dict:
            different_names.append(item['name'])
    print(different_names)  # 输出: ['Alice', 'Bob']
    
    
    #使用列表推导式 (更简洁)
    names_in_data2 = {item['name'] for item in data2}
    different_names = [item['name'] for item in data1 if item['name'] not in names_in_data2]
    print(different_names)  # 输出: ['Alice', 'Bob']