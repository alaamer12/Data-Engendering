"""
Apache Kafka with ZooKeeper handler.
"""

from pathlib import Path
from _manage._base import ToolHandler


class KafkaZookeeperHandler(ToolHandler):
    def __init__(self, base_dir: str):
        super().__init__(
            tool_name="Kafka (ZooKeeper)",
            tool_dir=Path(base_dir) / "kafka_zookeeper",
            ports={
                "ZooKeeper": 2181,
                "Kafka Broker": 9093,
                "Kafka UI": 8081
            }
        )
    
    def get_subdirectories(self):
        return ["exercises", "data", "logs", "config", "zookeeper-data"]
    
    def _tool_specific_setup(self) -> bool:
        """Create Kafka with ZooKeeper docker-compose.yml"""
        docker_compose_content = """version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.0
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
      ZOOKEEPER_SYNC_LIMIT: 2
    volumes:
      - ./zookeeper-data:/var/lib/zookeeper/data
      - ./logs/zookeeper:/var/log/zookeeper
    networks:
      - kafka-network

  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: kafka-zookeeper
    ports:
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_NUM_PARTITIONS: 3
    volumes:
      - ./data:/var/lib/kafka/data
      - ./logs/kafka:/var/log/kafka
    depends_on:
      - zookeeper
    networks:
      - kafka-network

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui-zk
    ports:
      - "8081:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local-zk
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9093
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
      DYNAMIC_CONFIG_ENABLED: 'true'
    depends_on:
      - kafka
      - zookeeper
    networks:
      - kafka-network

networks:
  kafka-network:
    driver: bridge
"""
        
        with open(self.docker_compose_file, 'w') as f:
            f.write(docker_compose_content)
        
        return True
    
    def _wait_for_health(self) -> bool:
        """Wait for Kafka and ZooKeeper to be ready"""
        from _manage._docker_utils import wait_for_url
        import time
        
        # Wait for services to initialize
        time.sleep(15)
        
        # Check if Kafka UI is accessible
        return wait_for_url("http://localhost:8081", timeout=60)
