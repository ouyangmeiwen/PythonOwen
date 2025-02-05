#pip install kafka-python


from kafka import KafkaProducer, KafkaConsumer
import json

class KafkaClient:
    def __init__(self, brokers, topic, group_id=None):
        self.brokers = brokers
        self.topic = topic
        self.group_id = group_id

        # 初始化 Kafka 生产者
        self.producer = KafkaProducer(bootstrap_servers=self.brokers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        # 初始化 Kafka 消费者
        self.consumer = KafkaConsumer(self.topic,
                                      bootstrap_servers=self.brokers,
                                      group_id=self.group_id,
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    def produce_message(self, message):
        # 将消息发送到 Kafka
        self.producer.send(self.topic, message)
        print(f"Produced message: {message}")

    def consume_messages(self):
        # 从 Kafka 消费消息
        for msg in self.consumer:
            print(f"Consumed message: {msg.value} on topic {msg.topic}")

    def stop(self):
        # 关闭 Kafka 客户端
        self.producer.close()
        self.consumer.close()


if __name__ == "__main__":
    brokers = ["localhost:9092"]
    topic = "test_topic"

    # 创建 Kafka 客户端
    kafka_client = KafkaClient(brokers, topic, group_id="test_group")

    # 生产一条消息
    kafka_client.produce_message({"key": "value", "data": "Hello Kafka!"})

    # 启动消费者
    print("Consuming messages:")
    kafka_client.consume_messages()

    # 关闭客户端
    kafka_client.stop()
