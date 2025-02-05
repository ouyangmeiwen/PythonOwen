

class Result:
    def __init__(self, success: bool, message: str = "", data: any = None, code: int = 200):
        """
        初始化统一的返回对象。

        :param success: 是否成功（True 或 False）
        :param message: 返回信息（提示信息或错误信息）
        :param data: 返回数据（字典、列表或其他数据对象）
        :param code: HTTP 状态码或业务自定义状态码，默认为 200
        """
        self.success = success
        self.message = message
        self.data = data
        self.code = code

    def to_dict(self):
        """
        转换为字典格式，便于序列化为 JSON。
        """
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "code": self.code,
        }

    def __repr__(self):
        """
        返回对象的字符串表示（JSON 格式）。
        """
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    @staticmethod
    def success_result(data: any = None, message: str = "Operation successful", code: int = 200):
        """
        快捷创建成功返回对象。

        :param data: 返回数据
        :param message: 成功信息
        :param code: 状态码
        :return: Result 对象
        """
        return Result(success=True, message=message, data=data, code=code)

    @staticmethod
    def error_result(message: str = "Operation failed", code: int = 400):
        """
        快捷创建失败返回对象。

        :param message: 错误信息
        :param code: 状态码
        :return: Result 对象
        """
        return Result(success=False, message=message, code=code)

# 示例用法
if __name__ == "__main__":
    # 成功返回示例
    success_response = Result.success_result(data={"id": 123, "name": "example"}, message="Data fetched successfully")
    print(success_response)

    # 失败返回示例
    error_response = Result.error_result(message="Invalid input", code=422)
    print(error_response)
