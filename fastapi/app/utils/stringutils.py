import uuid
import hashlib
import re

class StringUtils:

    @staticmethod
    def to_bool(value):
        """
        将输入值转换为布尔值。
        支持字节串和其他类型。

        :param value: 待转换的值，可以是字节串、数字或其他类型
        :return: 转换后的布尔值
        """
        if isinstance(value, bytes):
            return value == b'\x01'  # b'\x01' 表示 True，b'\x00' 表示 False
        return bool(value)  # 对于其他类型，直接转换为布尔值


    @staticmethod
    def is_empty(string):
        """判断字符串是否为空"""
        return not string or string.strip() == ""

    @staticmethod
    def to_upper(string):
        """将字符串转换为大写"""
        return string.upper()

    @staticmethod
    def to_lower(string):
        """将字符串转换为小写"""
        return string.lower()

    @staticmethod
    def reverse(string):
        """反转字符串"""
        return string[::-1]

    @staticmethod
    def remove_whitespace(string):
        """移除字符串中的所有空格"""
        return string.replace(" ", "")

    @staticmethod
    def replace_substring(string, old, new):
        """替换字符串中的子字符串"""
        return string.replace(old, new)

    @staticmethod
    def starts_with(string, prefix):
        """检查字符串是否以指定前缀开头"""
        return string.startswith(prefix)

    @staticmethod
    def ends_with(string, suffix):
        """检查字符串是否以指定后缀结尾"""
        return string.endswith(suffix)

    @staticmethod
    def split_string(string, delimiter=" "):
        """按指定分隔符分割字符串"""
        return string.split(delimiter)

    @staticmethod
    def join_strings(string_list, delimiter=" "):
        """使用指定的分隔符将字符串列表连接成一个字符串"""
        return delimiter.join(string_list)

    @staticmethod
    def capitalize_words(string):
        """将字符串中的每个单词首字母大写"""
        return string.title()

    @staticmethod
    def contains_substring(string, substring):
        """检查字符串是否包含子字符串"""
        return substring in string

    @staticmethod
    def get_length(string):
        """返回字符串的长度"""
        return len(string)

    @staticmethod
    def find_substring(string, substring):
        """返回子字符串首次出现的位置"""
        return string.find(substring)

    @staticmethod
    def is_palindrome(string):
        """检查字符串是否是回文"""
        return string == string[::-1]

    @staticmethod
    def left_trim(string):
        """去掉字符串左侧的空格"""
        return string.lstrip()

    @staticmethod
    def right_trim(string):
        """去掉字符串右侧的空格"""
        return string.rstrip()

    @staticmethod
    def count_occurrences(string, substring):
        """计算子字符串出现的次数"""
        return string.count(substring)

    @staticmethod
    def remove_substring(string, substring):
        """移除字符串中的指定子字符串"""
        return string.replace(substring, "")

    @staticmethod
    def format_string(string, *args, **kwargs):
        """格式化字符串"""
        return string.format(*args, **kwargs)

    @staticmethod #非静态类下面的方法要加上self
    def truncate_string(s, max_length):
        if isinstance(s, str):
            if len(s) > max_length:
                return s[:max_length] + '...'
            return s
        return s
    
    #格式化字符串只允许数字和字母
    @staticmethod #非静态类下面的方法要加上self
    def filter_string(input_string):
        # 定义正则表达式，匹配所有非字母和数字的字符
        pattern = re.compile('[^a-zA-Z0-9]')
        # 使用 sub 方法将匹配到的字符替换为空字符串
        filtered_string = pattern.sub('', input_string)
        return filtered_string

    #移除首尾[]
    @staticmethod #非静态类下面的方法要加上self
    def strip_string(input_string):
        stripped_string = input_string.strip("[]")
        return stripped_string

    @staticmethod
    def generate_uuid32():
        """
        生成 UUID32 格式（32 位，无连字符）
        """
        return uuid.uuid4().hex  # uuid4 生成一个随机 UUID，hex 返回去掉连字符的 32 位字符串
    @staticmethod
    def generate_uuid36():
        """
        生成 UUID36 格式（36 位，带连字符）
        """
        return str(uuid.uuid4())  # uuid4 生成一个随机 UUID，str 返回带连字符的 36 位字符串

if __name__ == "__main__":
    test_string = " hello world "

    # 1. 判断字符串是否为空
    print(StringUtils.is_empty(test_string))  # 输出: False
    print(StringUtils.is_empty("  "))  # 输出: True

    # 2. 将字符串转换为大写
    print(StringUtils.to_upper(test_string))  # 输出: " HELLO WORLD "

    # 3. 将字符串转换为小写
    print(StringUtils.to_lower(test_string))  # 输出: " hello world "

    # 4. 反转字符串
    print(StringUtils.reverse(test_string))  # 输出: " dlrow olleh "

    # 5. 移除字符串中的所有空格
    print(StringUtils.remove_whitespace(test_string))  # 输出: "helloworld"

    # 6. 替换字符串中的子字符串
    print(StringUtils.replace_substring(test_string, "world", "Python"))  # 输出: " hello Python "

    # 7. 检查字符串是否以指定前缀开头
    print(StringUtils.starts_with(test_string, "hello"))  # 输出: True
    print(StringUtils.starts_with(test_string, "world"))  # 输出: False

    # 8. 检查字符串是否以指定后缀结尾
    print(StringUtils.ends_with(test_string, "world"))  # 输出: True
    print(StringUtils.ends_with(test_string, "hello"))  # 输出: False

    # 9. 按指定分隔符分割字符串
    print(StringUtils.split_string(test_string))  # 输出: ['hello', 'world']
    print(StringUtils.split_string(test_string, "o"))  # 输出: [' hell', ' w', 'rld ']

    # 10. 使用指定的分隔符将字符串列表连接成一个字符串
    print(StringUtils.join_strings(['hello', 'world'], "-"))  # 输出: "hello-world"

    # 11. 将字符串中的每个单词首字母大写
    print(StringUtils.capitalize_words(test_string))  # 输出: "Hello World"

    # 12. 检查字符串是否包含子字符串
    print(StringUtils.contains_substring(test_string, "world"))  # 输出: True
    print(StringUtils.contains_substring(test_string, "Python"))  # 输出: False

    # 13. 返回字符串的长度
    print(StringUtils.get_length(test_string))  # 输出: 13

    # 14. 返回子字符串首次出现的位置
    print(StringUtils.find_substring(test_string, "world"))  # 输出: 6
    print(StringUtils.find_substring(test_string, "Python"))  # 输出: -1

    # 15. 检查字符串是否是回文
    print(StringUtils.is_palindrome("madam"))  # 输出: True
    print(StringUtils.is_palindrome("hello"))  # 输出: False

    # 16. 去掉字符串左侧的空格
    print(StringUtils.left_trim(test_string))  # 输出: "hello world "

    # 17. 去掉字符串右侧的空格
    print(StringUtils.right_trim(test_string))  # 输出: " hello world"

    # 18. 计算子字符串出现的次数
    print(StringUtils.count_occurrences(test_string, "o"))  # 输出: 2

    # 19. 移除字符串中的指定子字符串
    print(StringUtils.remove_substring(test_string, "world"))  # 输出: " hello "

    # 20. 格式化字符串
    print(StringUtils.format_string("Hello, {}!", "Alice"))  # 输出: "Hello, Alice!"
