# Apache Kafka with ZooKeeper Practice Guide

## Overview

This is the traditional Kafka setup with ZooKeeper. Use this for:
- Learning about ZooKeeper's role in Kafka
- Compatibility with legacy systems
- Understanding migration to KRaft mode

## Access Information

After running `python manager.py start kafka_zookeeper`:
- **Kafka Broker**: `localhost:9093`
- **ZooKeeper**: `localhost:2181`
- **Kafka UI**: http://localhost:8081

## Quick Start

```bash
python manager.py setup kafka_zookeeper
python manager.py start kafka_zookeeper
```

## Key Differences from KRaft Mode

- **ZooKeeper Dependency**: Requires ZooKeeper for metadata management
- **Different Port**: Broker on 9093 (vs 9092 for KRaft)
- **Legacy Architecture**: Traditional Kafka deployment model
- **Migration Path**: Can migrate to KRaft in future

## ZooKeeper Commands

```bash
# Connect to ZooKeeper CLI
docker exec -it zookeeper zkCli.sh

# List Kafka nodes
ls /brokers/ids

# View broker details
get /brokers/ids/1
```

## Practice Exercises

Same as Kafka KRaft mode, but use port 9093 for broker connection.

## Resources

- [ZooKeeper Documentation](https://zookeeper.apache.org/doc/current/)
- [Kafka + ZooKeeper Guide](https://kafka.apache.org/documentation/#zk)
