import requests
from typing import Any, Dict, Optional

class HttpClient:
    """封装常见的 HTTP 请求"""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

    def _send_request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """发送 HTTP 请求"""
        url = self.base_url + url
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()  # 如果响应状态码不是 2xx, 会抛出 HTTPError
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """发送 GET 请求"""
        response = self._send_request('GET', url, params=params, headers=headers)
        if response:
            return response.json()  # 返回 JSON 响应内容
        return None

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """发送 POST 请求"""
        response = self._send_request('POST', url, data=data, headers=headers)
        if response:
            return response.json()  # 返回 JSON 响应内容
        return None

    def put(self, url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """发送 PUT 请求"""
        response = self._send_request('PUT', url, data=data, headers=headers)
        if response:
            return response.json()  # 返回 JSON 响应内容
        return None

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """发送 DELETE 请求"""
        response = self._send_request('DELETE', url, headers=headers)
        if response:
            return response.json()  # 返回 JSON 响应内容
        return None

# 使用示例
if __name__ == "__main__":
    # 创建一个 HTTP 客户端对象
    client = HttpClient(base_url="https://jsonplaceholder.typicode.com")

    # 设置请求头部
    headers = {
        "Content-Type": "application/json",  # 设置请求体格式
        "Authorization": "Bearer YOUR_TOKEN"  # 示例的授权头
    }

    # 发送 GET 请求
    response = client.get("/posts/1", headers=headers)
    print("GET Response:", response)

    # 发送 POST 请求
    new_data = {"title": "foo", "body": "bar", "userId": 1}
    response = client.post("/posts", data=new_data, headers=headers)
    print("POST Response:", response)

    # 发送 PUT 请求
    updated_data = {"id": 1, "title": "foo_updated", "body": "bar_updated", "userId": 1}
    response = client.put("/posts/1", data=updated_data, headers=headers)
    print("PUT Response:", response)

    # 发送 DELETE 请求
    response = client.delete("/posts/1", headers=headers)
    print("DELETE Response:", response)
