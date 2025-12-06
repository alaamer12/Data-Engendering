# Apache Kafka (KRaft Mode) Practice Guide

## Overview

Apache Kafka is a distributed event streaming platform. This setup uses **KRaft mode** (no ZooKeeper required), the modern Kafka architecture.

## Access Information

After running `python manager.py start kafka`:
- **Kafka Broker**: `localhost:9092`
- **Kafka UI**: http://localhost:8080

## Quick Start

```bash
# Setup and start
python manager.py setup kafka
python manager.py start kafka

# Check status
python manager.py status kafka

# Stop
python manager.py stop kafka
```

## Practice Exercises

### Exercise 1: Topic Management

```bash
# Enter Kafka container
docker exec -it kafka-kraft bash

# Create a topic
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic --partitions 3 --replication-factor 1

# List topics
kafka-topics.sh --bootstrap-server localhost:9092 --list

# Describe topic
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic test-topic

# Delete topic
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic test-topic
```

### Exercise 2: Producer & Consumer (Console)

```bash
# Terminal 1: Start a console producer
docker exec -it kafka-kraft kafka-console-producer.sh --bootstrap-server localhost:9092 --topic messages

# Type messages and press Enter
# Terminal 2: Start a console consumer
docker exec -it kafka-kraft kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic messages --from-beginning
```

### Exercise 3: Python Producer

Create `exercises/producer.py`:

```python
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send messages
for i in range(10):
    message = {'id': i, 'value': f'Message {i}', 'timestamp': time.time()}
    producer.send('python-topic', value=message)
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()
producer.close()
```

### Exercise 4: Python Consumer

Create `exercises/consumer.py`:

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'python-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Waiting for messages...")
for message in consumer:
    print(f"Received: {message.value}")
```

### Exercise 5: Consumer Groups

```bash
# Start multiple consumers in the same group
# Terminal 1
docker exec -it kafka-kraft kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic messages --group my-group

# Terminal 2
docker exec -it kafka-kraft kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic messages --group my-group

# Produce messages and see them distributed across consumers
```

## Project Ideas

1. **Log Aggregator**: Collect logs from multiple services into Kafka topics
2. **Event Sourcing**: Build an event-driven application with Kafka as the event store
3. **Real-time Metrics**: Stream application metrics to Kafka for monitoring
4. **Data Replication**: Use Kafka to replicate data between systems

## Key Concepts

- **Topics**: Categories for messages
- **Partitions**: Parallel processing units within a topic
- **Producers**: Applications that send messages
- **Consumers**: Applications that read messages
- **Consumer Groups**: Load balancing across multiple consumers
- **Offsets**: Position in the message log

## Monitoring

Use Kafka UI at http://localhost:8080 to:
- View topics and partitions
- Monitor consumer lag
- Inspect messages
- Check broker health

## Troubleshooting

```bash
# View logs
docker-compose -f kafka/docker-compose.yml logs -f

# Check broker status
docker exec -it kafka-kraft kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Reset consumer group offset
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --reset-offsets --to-earliest --topic messages --execute
```

## Resources

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [KRaft Mode Overview](https://kafka.apache.org/documentation/#kraft)
- [Python Kafka Client](https://kafka-python.readthedocs.io/)
