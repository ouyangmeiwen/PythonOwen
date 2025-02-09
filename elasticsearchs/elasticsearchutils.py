from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError, ConnectionError, TransportError, AuthenticationException
from elasticsearch.helpers import bulk

class ElasticsearchClient:
    def __init__(self, host='localhost', port=9200, scheme='http'):
        # 初始化 Elasticsearch 客户端
        self.es = Elasticsearch([{'host': host, 'port': port, 'scheme': scheme}])

        if not self.es.ping():
            raise Exception("Elasticsearch cluster is not available")

    def create_index(self, index_name, body=None):
        # 创建索引
        if not self.es.indices.exists(index=index_name):
            try:
                self.es.indices.create(index=index_name, body=body or {})
                print(f"Index '{index_name}' created successfully.")
            except (RequestError, TransportError) as e:
                print(f"Error creating index '{index_name}': {e}")
    
    def index_document(self, index_name, doc_type, doc_id, body):
        # 插入文档
        try:
            response = self.es.index(index=index_name,  id=doc_id, body=body)
            print(f"Document indexed successfully: ID = {response['_id']}")
        except (RequestError, TransportError) as e:
            print(f"Error indexing document: {e}")

    def bulk_index_documents(self, index_name, doc_type, documents):
        # 批量插入文档
        actions = []
        for doc in documents:
            action = {
                "_op_type": "index",
                "_index": index_name,
                "_type": doc_type,
                "_id": doc.get('id'),
                "_source": doc
            }
            actions.append(action)
        
        try:
            response = self.es.bulk(body=actions)
            print(f"Bulk indexing completed: {response}")
        except (RequestError, TransportError) as e:
            print(f"Error bulk indexing: {e}")
    
    def get_document(self, index_name, doc_type, doc_id):
        # 获取文档
        try:
            response = self.es.get(index=index_name,  id=doc_id)
            return response['_source']
        except NotFoundError:
            print(f"Document with ID {doc_id} not found.")
        except (RequestError, TransportError) as e:
            print(f"Error fetching document: {e}")
    
    def search(self, index_name, query, size=10):
        # 搜索文档
        try:
            response = self.es.search(index=index_name, body=query, size=size)
            return [hit['_source'] for hit in response['hits']['hits']]
        except (RequestError, TransportError) as e:
            print(f"Error searching: {e}")
            return []
    
    def search_by_id(self, index_name, doc_id):
        # 根据ID搜索文档
        try:
            response = self.es.get(index=index_name, id=doc_id)
            return response['_source']
        except NotFoundError:
            print(f"Document with ID {doc_id} not found.")
        except (RequestError, TransportError) as e:
            print(f"Error searching by ID: {e}")
    
    def delete_document(self, index_name, doc_type, doc_id):
        # 删除文档
        try:
            response = self.es.delete(index=index_name,  id=doc_id)
            print(f"Document with ID {doc_id} deleted successfully.")
        except NotFoundError:
            print(f"Document with ID {doc_id} not found.")
        except (RequestError, TransportError) as e:
            print(f"Error deleting document: {e}")
    
    def delete_index(self, index_name):
        # 删除索引
        try:
            if self.es.indices.exists(index=index_name):
                self.es.indices.delete(index=index_name)
                print(f"Index '{index_name}' deleted successfully.")
            else:
                print(f"Index '{index_name}' does not exist.")
        except (RequestError, TransportError) as e:
            print(f"Error deleting index '{index_name}': {e}")

    def update_document_value(self, index_name, doc_id, body):
        # 更新文档
        try:
            response = self.es.update(index=index_name, id=doc_id, body={
                "doc": body  # 只更新给定的字段
            })
            print(f"Document with ID {doc_id} updated successfully.")
        except (RequestError, TransportError) as e:
            print(f"Error updating document: {e}")

    def replace_document(self, index_name, doc_id, body):
        # 完全替换文档
        try:
            response = self.es.index(index=index_name, id=doc_id, body=body)
            print(f"Document with ID {doc_id} replaced successfully.")
        except (RequestError, TransportError) as e:
            print(f"Error replacing document: {e}")

    def update_document_with_script(self, index_name, doc_id, script):
        # 使用脚本更新文档
        try:
            response = self.es.update(index=index_name, id=doc_id, body={
                "script": {
                    "source": script  # 脚本内容，用于修改文档
                }
            })
            print(f"Document with ID {doc_id} updated using script.")
        except (RequestError, TransportError) as e:
            print(f"Error updating document with script: {e}")

    def bulk_update_documents(self, index_name, documents):
        #批量更新
        actions = []
        for doc in documents:
            action = {
                "_op_type": "update",  # 使用更新操作
                "_index": index_name,
                "_id": doc["id"],
                "doc": doc["body"]  # 需要更新的字段
            }
            actions.append(action)

        try:
            bulk(self.es, actions)
            print(f"Bulk update completed.")
        except Exception as e:
            print(f"Error in bulk update: {e}")


# 使用示例
if __name__ == "__main__":
    # 创建 Elasticsearch 客户端实例
    es_client = ElasticsearchClient(host='localhost', port=9200)

    # 创建索引
    index_name = "my_index"
    es_client.create_index(index_name)

    # 插入文档
    doc_id = "1"
    doc_body = {"name": "John", "age": 30}
    es_client.index_document(index_name, '_doc', doc_id, doc_body)


    update_body = {"age": 31}  # 只更新 age 字段
    es_client.update_document_value(index_name, doc_id, update_body)

    new_doc_body = {"name": "John", "age": 31}  # 完全替换文档
    es_client.replace_document(index_name, doc_id, new_doc_body)

    script = "ctx._source.age += 1"  # 将 age 字段增加 1
    es_client.update_document_with_script(index_name, doc_id, script)

    documents_to_update = [
        {"id": "1", "body": {"age": 32}},  # 更新 ID 为 1 的文档，修改 age 字段
        {"id": "2", "body": {"age": 28}}   # 更新 ID 为 2 的文档，修改 age 字段
    ]
    es_client.bulk_update_documents(index_name, documents_to_update)


    # 查询文档
    query = {
        "query": {
            "match": {
                "name": "John"
            }
        }
    }
    results = es_client.search(index_name, query)
    print("Search Results:", results)


    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "wildcard": {
                            "name": "*John*"  # Name containing "John" anywhere
                        }
                    }
                ],
                "filter": [
                    {
                        "range": {
                            "age": {
                                "gt": 25  # Age greater than 25
                            }
                        }
                    }
                ]
            }
        }
    }

    results = es_client.search(index_name, query)
    print("Search Results:", results)



    # 获取文档
    document = es_client.get_document(index_name, '_doc', doc_id)
    print("Document:", document)

    # 批量插入文档
    bulk_docs = [
        {"id": "2", "name": "Jane", "age": 25},
        {"id": "3", "name": "Mike", "age": 35}
    ]
    es_client.bulk_index_documents(index_name, '_doc', bulk_docs)

    # 删除文档
    es_client.delete_document(index_name, '_doc', doc_id)

    # 删除索引
    es_client.delete_index(index_name)
