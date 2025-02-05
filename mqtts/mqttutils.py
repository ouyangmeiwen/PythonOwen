import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, broker_address, username=None, password=None, port=1883, keep_alive_interval=60):
        self.broker_address = broker_address
        self.username = username
        self.password = password
        self.port = port
        self.keep_alive_interval = keep_alive_interval
        self.client = mqtt.Client()

        # 设置回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe

        # 如果提供了用户名和密码，设置认证信息
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to {self.broker_address} with result code {rc}")
        # 在连接成功后订阅主题
        self.client.subscribe("test/topic")

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"Subscribed with QoS {granted_qos}")

    def connect(self):
        # 连接到MQTT代理服务器
        print(f"Connecting to broker {self.broker_address}...")
        self.client.connect(self.broker_address, self.port, self.keep_alive_interval)
        self.client.loop_start()  # 启动后台线程，处理网络通讯

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()  # 停止后台线程

    def publish(self, topic, message, qos=0, retain=False):
        # 发布消息
        self.client.publish(topic, message, qos, retain)

    def subscribe(self, topic, qos=0):
        # 订阅主题
        self.client.subscribe(topic, qos)

    def unsubscribe(self, topic):
        # 取消订阅
        self.client.unsubscribe(topic)


if __name__ == "__main__":
    # 示例：使用封装的 MqttClient，并传入用户名和密码
    mqtt_client = MqttClient("mqtt.eclipse.org", username="your_username", password="your_password")
    mqtt_client.connect()

    # 发布一条消息
    mqtt_client.publish("test/topic", "Hello MQTT with Authentication!")

    # 等待消息接收
    import time
    time.sleep(5)

    # 断开连接
    mqtt_client.disconnect()
