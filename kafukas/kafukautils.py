from kafka import KafkaProducer, KafkaConsumer
import json
import threading
import time

class KafkaClient:
    def __init__(self, brokers, topic, group_id=None):
        self.brokers = brokers
        self.topic = topic
        self.group_id = group_id

        # 初始化 Kafka 生产者，增加 acks 参数来启用消息确认
        self.producer = KafkaProducer(bootstrap_servers=self.brokers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                      acks='all',  # acks='all' 表示等待所有副本确认
                                      retries=3)   # 在发送失败时重试3次

        # 初始化 Kafka 消费者
        self.consumer = KafkaConsumer(self.topic,
                                      bootstrap_servers=self.brokers,
                                      group_id=self.group_id,
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    def produce_message(self, message):
        # 将消息发送到 Kafka，并等待确认
        future = self.producer.send(self.topic, message)
        try:
            # 等待消息发送并确认成功
            record_metadata = future.get(timeout=10)  # 设置超时时间为10秒
            print(f"Produced message: {message} to topic: {record_metadata.topic}, partition: {record_metadata.partition}, offset: {record_metadata.offset}")
        except Exception as e:
            print(f"Error producing message: {e}")

    def consume_messages(self):
        # 从 Kafka 消费消息
        for msg in self.consumer:
            print(f"Consumed message: {msg.value} on topic {msg.topic}")

    def stop(self):
        # 关闭 Kafka 客户端
        self.producer.close()
        self.consumer.close()

def start_consuming(kafka_client):
    # 在新线程中启动消息消费
    print("Starting to consume messages in the background...")
    kafka_client.consume_messages()

if __name__ == "__main__":
    brokers = ["localhost:9092"]
    topic = "test_topic"

    # 创建 Kafka 客户端
    kafka_client = KafkaClient(brokers, topic, group_id="test_group")

    # 启动消费者线程
    consumer_thread = threading.Thread(target=start_consuming, args=(kafka_client,))
    consumer_thread.daemon = True  # 设置为守护线程，主线程退出时也会退出
    consumer_thread.start()

    # 生产几条消息
    kafka_client.produce_message({"key": "value", "data": "Hello Kafka 1!"})
    time.sleep(1)  # 等待消费者消费一些消息

    kafka_client.produce_message({"key": "value", "data": "Hello Kafka 2!"})
    time.sleep(1)

    # 主线程继续生产消息，或者退出
    print("Main thread continues to run, producing more messages...")
    kafka_client.produce_message({"key": "value", "data": "Hello Kafka 3!"})

    # 等待消费者消费消息，给线程一些时间
    time.sleep(5)

    # 关闭客户端
    kafka_client.stop()
    print("Kafka client stopped.")
