import json
from typing import Any, Dict

class JsonUitls:
    @staticmethod
    def serialize_to_json(obj: Any) -> str:
        """将 Python 对象序列化为 JSON 字符串"""
        try:
            return json.dumps(obj, indent=4)
        except (TypeError, ValueError) as e:
            print(f"Error serializing object: {e}")
            return ''
    @staticmethod
    def deserialize_from_json(json_string: str) -> Any:
        """将 JSON 字符串反序列化为 Python 对象"""
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error deserializing JSON: {e}")
            return None
    @staticmethod
    def read_json(file_path):
        """读取 JSON 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def write_json(file_path, data):
        """写入数据到 JSON 文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


# 测试用例
if __name__ == "__main__":
    # 测试序列化
    data = {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }

    # 序列化
    serialized_data = JsonUitls.serialize_to_json(data)
    print("Serialized JSON:")
    print(serialized_data)

    # 测试反序列化
    json_data = '{"name": "Alice", "age": 30, "city": "New York"}'
    deserialized_data = JsonUitls.deserialize_from_json(json_data)
    print("\nDeserialized Data:")
    print(deserialized_data)
