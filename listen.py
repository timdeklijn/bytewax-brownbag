from confluent_kafka import Consumer

consumer = Consumer({"bootstrap.servers":"localhost:9092", "group.id": "group1"})
consumer.subscribe(["test-topic"])
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    print('Received message: {}'.format(msg.value().decode('utf-8')))
