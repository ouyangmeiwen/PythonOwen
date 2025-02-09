#pip install pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from typing import List, Dict, Any

class MongoDBClient:
    def __init__(self, uri: str, db_name: str):
        # 连接到 MongoDB 数据库
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        """
        向指定集合中插入文档
        """
        collection = self.db[collection_name]
        try:
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except DuplicateKeyError as e:
            return f"Duplicate key error: {e}"
        except PyMongoError as e:
            return f"Error occurred: {e}"

    def find_document(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        查找指定条件的文档
        """
        collection = self.db[collection_name]
        documents = list(collection.find(query))
        return documents

    def update_document(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> str:
        """
        更新指定条件的文档
        """
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update})
        if result.matched_count == 0:
            return "No document matched the query"
        return f"Matched {result.matched_count} document(s), modified {result.modified_count} document(s)"

    def delete_document(self, collection_name: str, query: Dict[str, Any]) -> str:
        """
        删除指定条件的文档
        """
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        if result.deleted_count == 0:
            return "No document matched the query"
        return f"Deleted {result.deleted_count} document(s)"

    def close(self):
        """关闭连接"""
        self.client.close()

# 测试 MongoDB 操作类
if __name__ == "__main__":
    # MongoDB URI 和数据库名称
    uri = "mongodb://rootuser:rootpassword@localhost:27017/"
    db_name = "test_db"

    # 创建 MongoDB 客户端
    db_client = MongoDBClient(uri, db_name)

    # 测试：插入文档
    doc = {"name": "John Doe", "age": 29, "city": "New York"}
    inserted_id = db_client.insert_document("users", doc)
    print(f"Inserted document with ID: {inserted_id}")

    # 测试：查询文档
    query = {"name": "John Doe"}
    result = db_client.find_document("users", query)
    print(f"Found documents: {result}")

    # 测试：更新文档
    update = {"age": 30}
    update_result = db_client.update_document("users", query, update)
    print(update_result)

    # 测试：删除文档
    delete_result = db_client.delete_document("users", query)
    print(delete_result)

    # 关闭连接
    db_client.close()
